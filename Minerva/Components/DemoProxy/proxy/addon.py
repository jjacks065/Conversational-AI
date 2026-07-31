"""Mitmproxy addon for strict, fail-open JSON response transformation."""

from __future__ import annotations

import json
import os
import sys
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Protocol

from mitmproxy import ctx, exceptions, http
from mitmproxy.addonmanager import Loader

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from proxy import __version__
from proxy.config import AppConfig, ConfigError, load_config
from proxy.health import HealthServer, HealthState
from proxy.logging_config import StructuredLogger
from proxy.matcher import RequestMetadata, ResponseMatcher, ResponseMetadata
from proxy.pac_server import PacServer, render_pac
from proxy.transformer import transform_payload


PROXY_VERSION = __version__
DEFAULT_CONFIG_PATH = _PROJECT_ROOT / "config" / "proxy.yaml"
PAC_TEMPLATE_PATH = _PROJECT_ROOT / "pac" / "demo-proxy.pac"
_REQUIRED_RESPONSE_FIELDS = ("questionId", "sessionId", "content", "responseId")


class InvalidResponseSchema(ValueError):
    """Raised when a matched JSON body does not satisfy the response contract."""


class ResponseTooLarge(ValueError):
    """Raised when a response exceeds the configured transformation buffer."""


class MissingResponseBody(ValueError):
    """Raised when a matched response does not contain a buffered body."""


class EventLogger(Protocol):
    def emit(self, **event: Any) -> None: ...


class ManagedHealthServer(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...


class ResponseTransformAddon:
    """Transform only eligible server-to-client buffered JSON responses."""

    def __init__(
        self,
        *,
        config: AppConfig | None = None,
        event_logger: EventLogger | None = None,
        health_state: HealthState | None = None,
        transformer: Callable[[dict[str, Any]], dict[str, Any]] = transform_payload,
        health_server_factory: Callable[
            [HealthState, int], ManagedHealthServer
        ] | None = None,
        pac_server_factory: Callable[[str, int], ManagedHealthServer] | None = None,
    ) -> None:
        self._config_injected = config is not None
        self._config: AppConfig | None = None
        self._matcher: ResponseMatcher | None = None
        self._event_logger = event_logger
        self._health_state = health_state
        self._health_server: ManagedHealthServer | None = None
        self._pac_server: ManagedHealthServer | None = None
        self._health_server_factory = health_server_factory or (
            lambda state, port: HealthServer(state, port=port)
        )
        self._pac_server_factory = pac_server_factory or (
            lambda content, port: PacServer(content, port=port)
        )
        self._transformer = transformer
        self._running = False
        if config is not None:
            self._activate_config(config)

    def load(self, loader: Loader) -> None:
        loader.add_option(
            "demo_proxy_config",
            str,
            str(DEFAULT_CONFIG_PATH),
            "Path to the Demo Response Proxy YAML configuration file.",
        )

    def configure(self, updated: set[str]) -> None:
        if self._config_injected:
            return
        if "demo_proxy_config" not in updated and self._config is not None:
            return
        try:
            config = load_config(Path(ctx.options.demo_proxy_config))
        except ConfigError as exc:
            raise exceptions.OptionsError(str(exc)) from exc
        self._activate_config(config)

    def running(self) -> None:
        if self._config is None:
            self._activate_config(load_config(DEFAULT_CONFIG_PATH))
        assert self._config is not None
        assert self._health_state is not None
        if self._pac_server is None:
            pac_content = render_pac(
                PAC_TEMPLATE_PATH,
                target_host=self._config.target.host,
                proxy_host=self._config.proxy.listen_host,
                proxy_port=self._config.proxy.listen_port,
            )
            self._pac_server = self._pac_server_factory(
                pac_content, self._config.platform.pac_port
            )
        if self._health_server is None:
            self._health_server = self._health_server_factory(
                self._health_state, self._config.platform.health_port
            )
        try:
            self._pac_server.start()
            self._health_state.set_pac_server_listening(True)
            self._health_server.start()
            self._health_state.set_proxy_listening(True)
            self._running = True
        except Exception:
            self._health_state.set_proxy_listening(False)
            self._health_state.set_pac_server_listening(False)
            self._health_server.stop()
            self._pac_server.stop()
            self._health_server = None
            self._pac_server = None
            raise

    def done(self) -> None:
        if self._health_state is not None:
            self._health_state.set_proxy_listening(False)
            self._health_state.set_pac_server_listening(False)
        if self._pac_server is not None:
            self._pac_server.stop()
        if self._health_server is not None:
            self._health_server.stop()
        self._pac_server = None
        self._health_server = None
        self._running = False

    def response(self, flow: http.HTTPFlow) -> None:
        if self._config is None or self._matcher is None or flow.response is None:
            return

        request_metadata = RequestMetadata(
            scheme=flow.request.scheme,
            host=flow.request.host,
            port=flow.request.port,
            method=flow.request.method,
            path=flow.request.path,
            headers=_headers_as_mapping(flow.request.headers),
        )
        response_metadata = ResponseMetadata(
            headers=_headers_as_mapping(flow.response.headers)
        )
        decision = self._matcher.evaluate(request_metadata, response_metadata)
        original_raw = flow.response.raw_content
        original_bytes = len(original_raw or b"")
        content_type = flow.response.headers.get("content-type", "")

        if not decision.matched:
            if self._config.logging.log_match_decisions:
                self._emit_event(
                    flow=flow,
                    match_result=decision.reason,
                    path_template=decision.path_pattern,
                    content_type=content_type,
                    duration_ms=0.0,
                    original_bytes=original_bytes,
                    transformed_bytes=original_bytes,
                    fail_open=False,
                    exception_category=None,
                )
            return

        assert self._health_state is not None
        self._health_state.record_match()
        original_headers = flow.response.headers.copy()
        started = time.perf_counter()
        transformed_bytes = original_bytes

        try:
            transformed_bytes = self._transform_response(flow.response)
        except Exception as exc:
            flow.response.headers = original_headers
            flow.response.raw_content = original_raw
            exception_category = type(exc).__name__
            self._health_state.record_transformation(
                success=False, exception_category=exception_category
            )
            self._emit_event(
                flow=flow,
                match_result=decision.reason,
                path_template=decision.path_pattern,
                content_type=content_type,
                duration_ms=(time.perf_counter() - started) * 1000,
                original_bytes=original_bytes,
                transformed_bytes=original_bytes,
                fail_open=True,
                exception_category=exception_category,
            )
            if not self._config.proxy.fail_open:
                raise
            return

        self._health_state.record_transformation(success=True)
        self._emit_event(
            flow=flow,
            match_result=decision.reason,
            path_template=decision.path_pattern,
            content_type=content_type,
            duration_ms=(time.perf_counter() - started) * 1000,
            original_bytes=original_bytes,
            transformed_bytes=transformed_bytes,
            fail_open=False,
            exception_category=None,
        )

    def _activate_config(self, config: AppConfig) -> None:
        was_running = self._running
        if self._health_server is not None:
            self._health_server.stop()
            self._health_server = None
        if self._pac_server is not None:
            self._pac_server.stop()
            self._pac_server = None
        self._config = config
        self._matcher = ResponseMatcher(config)
        platform_label = os.environ.get("DEMO_PROXY_PLATFORM", "unknown")
        if self._event_logger is None:
            self._event_logger = StructuredLogger(
                level=config.logging.level,
                platform_label=platform_label,
                proxy_version=PROXY_VERSION,
            )
        if self._health_state is None:
            self._health_state = HealthState(
                platform_label=platform_label,
                target_host=config.target.host,
                transformer_version=config.transformation.transformer_version,
                fail_open=config.proxy.fail_open,
            )
        self._health_state.set_configuration_loaded(True)
        certificate_trusted = os.environ.get(
            "DEMO_PROXY_CERTIFICATE_TRUSTED", "false"
        ).strip().lower() in {"1", "true", "yes"}
        self._health_state.set_certificate_trusted(certificate_trusted)
        if was_running:
            self.running()

    def _transform_response(self, response: http.Response) -> int:
        assert self._config is not None
        raw_content = response.raw_content
        if raw_content is None:
            raise MissingResponseBody("matched response body is not buffered")
        if len(raw_content) > self._config.proxy.max_buffer_bytes:
            raise ResponseTooLarge("raw response exceeds max_buffer_bytes")

        decoded_content = response.content
        if decoded_content is None:
            raise MissingResponseBody("matched response body is empty")
        if len(decoded_content) > self._config.proxy.max_buffer_bytes:
            raise ResponseTooLarge("decoded response exceeds max_buffer_bytes")
        text = response.get_text(strict=True)
        if text is None:
            raise MissingResponseBody("matched response body has no text")

        payload = json.loads(text, parse_constant=_reject_non_finite_constant)
        _validate_response_schema(payload)
        transformed = self._transformer(payload)
        _validate_response_schema(transformed)
        if transformed != payload:
            response.text = json.dumps(
                transformed,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            )
        return len(response.raw_content or b"")

    def _emit_event(
        self,
        *,
        flow: http.HTTPFlow,
        match_result: str,
        path_template: str | None,
        content_type: str,
        duration_ms: float,
        original_bytes: int,
        transformed_bytes: int,
        fail_open: bool,
        exception_category: str | None,
    ) -> None:
        if self._event_logger is None:
            return
        self._event_logger.emit(
            correlation_id=flow.id,
            match_result=match_result,
            method=flow.request.method,
            host=flow.request.host,
            path_template=path_template,
            status_code=flow.response.status_code if flow.response else 0,
            content_type=content_type,
            transformation_duration_ms=duration_ms,
            original_bytes=original_bytes,
            transformed_bytes=transformed_bytes,
            fail_open=fail_open,
            exception_category=exception_category,
        )


def _headers_as_mapping(headers: http.Headers) -> Mapping[str, str]:
    return {name: value for name, value in headers.items()}


def _validate_response_schema(payload: object) -> None:
    if not isinstance(payload, dict):
        raise InvalidResponseSchema("response must be a JSON object")
    for field in _REQUIRED_RESPONSE_FIELDS:
        if not isinstance(payload.get(field), str):
            raise InvalidResponseSchema(f"response field must be a string: {field}")


def _reject_non_finite_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not supported: {value}")


addons = [ResponseTransformAddon()]
