from __future__ import annotations

import copy
import json
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from mitmproxy import connection, http

from proxy.addon import InvalidResponseSchema, ResponseTransformAddon, ResponseTooLarge
from proxy.config import parse_config
from proxy.health import HealthState
from tests.unit.test_config import valid_config_mapping


class RecordingEventLogger:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def emit(self, **event: Any) -> None:
        self.events.append(event)


class FakeManagedServer:
    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


class FailingManagedServer(FakeManagedServer):
    def start(self) -> None:
        self.started = True
        raise RuntimeError("bind failed")


def response_payload(content: str = "alpha\n\nbeta") -> dict[str, str]:
    return {
        "questionId": "question-1",
        "sessionId": "session-1",
        "content": content,
        "responseId": "response-1",
    }


def make_flow(
    *,
    host: str = "api.example.com",
    path: str = "/api/chatbot/ask",
    method: str = "POST",
    origin: str = "https://demo.example.com",
    request_content_type: str = "application/json",
    response_content_type: str = "application/json; charset=utf-8",
    response_body: str | bytes | None = None,
    status_code: int = 200,
) -> http.HTTPFlow:
    client = connection.Client(
        peername=("127.0.0.1", 50_000),
        sockname=("127.0.0.1", 8080),
    )
    server = connection.Server(address=(host, 443))
    flow = http.HTTPFlow(client, server)
    flow.request = http.Request.make(
        method,
        f"https://{host}{path}",
        json.dumps({"message": "sensitive prompt"}),
        headers={
            "Content-Type": request_content_type,
            "Origin": origin,
            "Authorization": "Bearer secret-token",
        },
    )
    if response_body is None:
        response_body = json.dumps(response_payload())
    response_headers = http.Headers(
        [
            (b"Content-Type", response_content_type.encode()),
            (b"Set-Cookie", b"affinity=secret-one"),
            (b"Set-Cookie", b"affinitySameSite=secret-two"),
            (b"X-TraceId", b"trace-secret"),
        ]
    )
    flow.response = http.Response.make(status_code, response_body, response_headers)
    return flow


class ResponseTransformAddonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = parse_config(valid_config_mapping())
        self.logger = RecordingEventLogger()
        self.health = HealthState(
            platform_label="test-platform",
            target_host=self.config.target.host,
            transformer_version=self.config.transformation.transformer_version,
            fail_open=self.config.proxy.fail_open,
        )
        self.addon = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
        )

    def test_transforms_matching_json_without_modifying_request_or_other_fields(self) -> None:
        flow = make_flow()
        request_before = copy.deepcopy(flow.request.get_state())
        cookie_headers = flow.response.headers.get_all("set-cookie")

        self.addon.response(flow)

        self.assertEqual(flow.request.get_state(), request_before)
        # Content should have transformation marker at the end
        content = flow.response.json()["content"]
        self.assertIn('<span style="display:none;" data-transformed="true"></span>', content)
        self.assertIn("alpha", content)
        self.assertIn("beta", content)
        self.assertEqual(flow.response.json()["questionId"], "question-1")
        self.assertEqual(flow.response.headers.get_all("set-cookie"), cookie_headers)
        self.assertEqual(
            int(flow.response.headers["content-length"]),
            len(flow.response.raw_content),
        )
        self.assertEqual(self.logger.events[-1]["match_result"], "matched")
        self.assertFalse(self.logger.events[-1]["fail_open"])
        self.assertNotIn("sensitive prompt", json.dumps(self.logger.events))
        self.assertNotIn("secret-token", json.dumps(self.logger.events))
        self.assertNotIn("affinity=", json.dumps(self.logger.events))

    def test_nonmatching_flow_is_untouched(self) -> None:
        flow = make_flow(host="similar.api.example.com")
        raw_before = flow.response.raw_content
        headers_before = list(flow.response.headers.items(multi=True))

        self.addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(list(flow.response.headers.items(multi=True)), headers_before)
        self.assertEqual(self.logger.events[-1]["match_result"], "host")

    def test_transforms_gzip_and_preserves_content_encoding(self) -> None:
        flow = make_flow()
        flow.response.encode("gzip")

        self.addon.response(flow)

        self.assertEqual(flow.response.headers["content-encoding"], "gzip")
        # Content should have transformation marker at the end
        content = flow.response.json()["content"]
        self.assertIn('<span style="display:none;" data-transformed="true"></span>', content)
        self.assertIn("alpha", content)
        self.assertIn("beta", content)

    def test_invalid_json_fails_open_with_exact_body_and_headers(self) -> None:
        flow = make_flow(response_body=b"not-json")
        raw_before = flow.response.raw_content
        headers_before = list(flow.response.headers.items(multi=True))

        self.addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(list(flow.response.headers.items(multi=True)), headers_before)
        self.assertTrue(self.logger.events[-1]["fail_open"])
        self.assertEqual(self.logger.events[-1]["exception_category"], "JSONDecodeError")
        self.assertIn("Fail-open", self.health.status_html())

    def test_invalid_schema_fails_open(self) -> None:
        flow = make_flow(response_body=json.dumps({"content": 123}))

        self.addon.response(flow)

        self.assertEqual(self.logger.events[-1]["exception_category"], "InvalidResponseSchema")
        self.assertEqual(flow.response.json(), {"content": 123})

    def test_common_error_responses_remain_exactly_unchanged(self) -> None:
        for status_code in (401, 429, 500):
            with self.subTest(status_code=status_code):
                flow = make_flow(
                    status_code=status_code,
                    response_body=json.dumps({"error": "safe error category"}),
                )
                raw_before = flow.response.raw_content
                headers_before = list(flow.response.headers.items(multi=True))

                self.addon.response(flow)

                self.assertEqual(flow.response.raw_content, raw_before)
                self.assertEqual(
                    list(flow.response.headers.items(multi=True)), headers_before
                )
                self.assertEqual(
                    self.logger.events[-1]["exception_category"],
                    "InvalidResponseSchema",
                )

    def test_missing_streamed_body_fails_open(self) -> None:
        flow = make_flow()
        flow.response.raw_content = None

        self.addon.response(flow)

        self.assertIsNone(flow.response.raw_content)
        self.assertEqual(
            self.logger.events[-1]["exception_category"], "MissingResponseBody"
        )

    def test_corrupt_content_encoding_fails_open(self) -> None:
        flow = make_flow(response_body=b"not-gzip")
        flow.response.headers["content-encoding"] = "gzip"
        raw_before = flow.response.raw_content
        headers_before = list(flow.response.headers.items(multi=True))

        self.addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(list(flow.response.headers.items(multi=True)), headers_before)
        self.assertEqual(self.logger.events[-1]["exception_category"], "ValueError")

    def test_non_finite_json_fails_open(self) -> None:
        body = (
            '{"questionId":"q","sessionId":"s","content":"alpha\\n\\nbeta",'
            '"responseId":"r","usage":NaN}'
        )
        flow = make_flow(response_body=body)
        raw_before = flow.response.raw_content

        self.addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(self.logger.events[-1]["exception_category"], "ValueError")

    def test_oversize_response_fails_open_before_parsing(self) -> None:
        source = valid_config_mapping()
        source["proxy"]["max_buffer_bytes"] = 4  # type: ignore[index]
        addon = ResponseTransformAddon(
            config=parse_config(source),
            event_logger=self.logger,
            health_state=self.health,
        )
        flow = make_flow()
        raw_before = flow.response.raw_content

        addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(self.logger.events[-1]["exception_category"], "ResponseTooLarge")

    def test_oversize_decoded_response_fails_open(self) -> None:
        source = valid_config_mapping()
        source["proxy"]["max_buffer_bytes"] = 200  # type: ignore[index]
        addon = ResponseTransformAddon(
            config=parse_config(source),
            event_logger=self.logger,
            health_state=self.health,
        )
        payload = response_payload(content="a" * 2_000)
        flow = make_flow(response_body=json.dumps(payload))
        flow.response.encode("gzip")
        self.assertLess(len(flow.response.raw_content or b""), 200)
        raw_before = flow.response.raw_content

        addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(self.logger.events[-1]["exception_category"], "ResponseTooLarge")

    def test_transformer_exception_fails_open(self) -> None:
        def raise_transformer(payload: dict[str, Any]) -> dict[str, Any]:
            raise RuntimeError("do not log sensitive payload")

        addon = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
            transformer=raise_transformer,
        )
        flow = make_flow()
        raw_before = flow.response.raw_content

        addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(self.logger.events[-1]["exception_category"], "RuntimeError")

    def test_invalid_transformer_output_fails_open(self) -> None:
        addon = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
            transformer=lambda payload: {"content": 123},
        )
        flow = make_flow()
        raw_before = flow.response.raw_content

        addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)
        self.assertEqual(
            self.logger.events[-1]["exception_category"], "InvalidResponseSchema"
        )

    def test_fail_open_false_restores_then_reraises(self) -> None:
        source = valid_config_mapping()
        source["proxy"]["fail_open"] = False  # type: ignore[index]
        addon = ResponseTransformAddon(
            config=parse_config(source),
            event_logger=self.logger,
            health_state=self.health,
        )
        flow = make_flow(response_body=b"not-json")
        raw_before = flow.response.raw_content

        with self.assertRaises(json.JSONDecodeError):
            addon.response(flow)

        self.assertEqual(flow.response.raw_content, raw_before)

    def test_running_and_done_manage_health_lifecycle(self) -> None:
        fake_health_server = FakeManagedServer()
        fake_pac_server = FakeManagedServer()
        pac_calls: list[tuple[str, int]] = []

        def pac_factory(content: str, port: int) -> FakeManagedServer:
            pac_calls.append((content, port))
            return fake_pac_server

        addon = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
            health_server_factory=lambda state, port: fake_health_server,
            pac_server_factory=pac_factory,
        )

        addon.running()
        running_payload = self.health.health_payload()
        addon.done()

        self.assertTrue(fake_health_server.started)
        self.assertTrue(fake_health_server.stopped)
        self.assertTrue(fake_pac_server.started)
        self.assertTrue(fake_pac_server.stopped)
        self.assertEqual(pac_calls[0][1], 8765)
        self.assertIn("api.example.com", pac_calls[0][0])
        self.assertTrue(running_payload["pacServerListening"])
        self.assertFalse(self.health.health_payload()["proxyListening"])
        self.assertFalse(self.health.health_payload()["pacServerListening"])

    def test_running_cleans_up_when_health_server_fails(self) -> None:
        fake_pac_server = FakeManagedServer()
        failing_health_server = FailingManagedServer()
        addon = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
            health_server_factory=lambda state, port: failing_health_server,
            pac_server_factory=lambda content, port: fake_pac_server,
        )

        with self.assertRaisesRegex(RuntimeError, "bind failed"):
            addon.running()

        self.assertTrue(fake_pac_server.stopped)
        self.assertTrue(failing_health_server.stopped)
        self.assertFalse(self.health.health_payload()["proxyListening"])
        self.assertFalse(self.health.health_payload()["pacServerListening"])

    def test_unconfigured_addon_and_flow_without_response_are_noops(self) -> None:
        addon = ResponseTransformAddon(
            event_logger=self.logger,
            health_state=self.health,
        )
        flow = make_flow()
        raw_before = flow.response.raw_content

        addon.response(flow)
        self.assertEqual(flow.response.raw_content, raw_before)

        configured = ResponseTransformAddon(
            config=self.config,
            event_logger=self.logger,
            health_state=self.health,
        )
        flow.response = None
        configured.response(flow)

    def test_load_registers_configuration_option(self) -> None:
        calls: list[tuple[Any, ...]] = []

        class Loader:
            def add_option(self, *args: Any, **kwargs: Any) -> None:
                calls.append((*args, kwargs))

        self.addon.load(Loader())

        self.assertEqual(calls[0][0], "demo_proxy_config")
        self.assertIs(calls[0][1], str)

    def test_configure_loads_yaml_without_mutating_mitmdump_listener_options(self) -> None:
        project_root = Path(__file__).resolve().parents[2]

        class Options:
            def __init__(self) -> None:
                self.demo_proxy_config = str(project_root / "config" / "proxy.yaml")

        options = Options()
        addon = ResponseTransformAddon(
            event_logger=self.logger,
            health_state=self.health,
        )

        with patch("proxy.addon.ctx", SimpleNamespace(options=options)):
            addon.configure({"demo_proxy_config"})

        self.assertTrue(self.health.health_payload()["configurationLoaded"])

    def test_configure_reports_certificate_trust_from_platform_verification(self) -> None:
        project_root = Path(__file__).resolve().parents[2]

        class Options:
            demo_proxy_config = str(project_root / "config" / "proxy.yaml")

        addon = ResponseTransformAddon(
            event_logger=self.logger,
            health_state=self.health,
        )
        with (
            patch.dict(os.environ, {"DEMO_PROXY_CERTIFICATE_TRUSTED": "true"}),
            patch("proxy.addon.ctx", SimpleNamespace(options=Options())),
        ):
            addon.configure({"demo_proxy_config"})

        self.assertTrue(self.health.health_payload()["certificateTrusted"])


if __name__ == "__main__":
    unittest.main()
