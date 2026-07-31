"""Loopback-only health and operator status reporting."""

from __future__ import annotations

import html
import json
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class HealthState:
    """Thread-safe operational metadata with no request or response content."""

    def __init__(
        self,
        *,
        platform_label: str,
        target_host: str,
        transformer_version: str,
        fail_open: bool,
    ) -> None:
        self._lock = threading.Lock()
        self._platform_label = platform_label
        self._target_host = target_host
        self._transformer_version = transformer_version
        self._fail_open = fail_open
        self._configuration_loaded = False
        self._proxy_listening = False
        self._pac_server_listening = False
        self._certificate_trusted = False
        self._last_matching_request: str | None = None
        self._last_transformation = "Never"

    def set_configuration_loaded(self, value: bool) -> None:
        with self._lock:
            self._configuration_loaded = bool(value)

    def set_proxy_listening(self, value: bool) -> None:
        with self._lock:
            self._proxy_listening = bool(value)

    def set_pac_server_listening(self, value: bool) -> None:
        with self._lock:
            self._pac_server_listening = bool(value)

    def set_certificate_trusted(self, value: bool) -> None:
        with self._lock:
            self._certificate_trusted = bool(value)

    def record_match(self) -> None:
        with self._lock:
            self._last_matching_request = datetime.now().astimezone().strftime("%H:%M:%S")

    def record_transformation(
        self, *, success: bool, exception_category: str | None = None
    ) -> None:
        with self._lock:
            if success:
                self._last_transformation = "Successful"
            else:
                category = exception_category or "UnknownError"
                self._last_transformation = f"Fail-open ({category})"

    def health_payload(self) -> dict[str, Any]:
        with self._lock:
            is_ok = (
                self._configuration_loaded
                and self._proxy_listening
                and self._pac_server_listening
                and self._certificate_trusted
            )
            return {
                "status": "ok" if is_ok else "degraded",
                "platform": self._platform_label,
                "proxyListening": self._proxy_listening,
                "pacServerListening": self._pac_server_listening,
                "configurationLoaded": self._configuration_loaded,
                "certificateTrusted": self._certificate_trusted,
                "targetHost": self._target_host,
                "transformerVersion": self._transformer_version,
            }

    def status_html(self) -> str:
        with self._lock:
            proxy = "Active" if self._proxy_listening else "Inactive"
            pac = "Active" if self._pac_server_listening else "Inactive"
            certificate = "Trusted" if self._certificate_trusted else "Unverified"
            last_match = self._last_matching_request or "Never"
            last_transformation = self._last_transformation
            fail_open = "Enabled" if self._fail_open else "Disabled"
        rows = (
            ("Proxy", proxy),
            ("PAC routing", pac),
            ("Certificate", certificate),
            ("Target rule", "Ready" if self._configuration_loaded else "Not ready"),
            ("Last matching request", last_match),
            ("Last transformation", last_transformation),
            ("Fail-open mode", fail_open),
        )
        items = "".join(
            f"<p>{html.escape(label)}: {html.escape(value)}</p>"
            for label, value in rows
        )
        return (
            "<!doctype html><html><head><meta charset=\"utf-8\">"
            "<title>Demo Response Proxy</title></head><body>"
            "<h1>Demo Response Proxy</h1>"
            f"{items}</body></html>"
        )


class HealthServer:
    """Serve health data only on IPv4 loopback."""

    def __init__(self, state: HealthState, *, port: int) -> None:
        self._state = state
        self._port = port
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def address(self) -> tuple[str, int]:
        if self._server is None:
            raise RuntimeError("health server is not running")
        host, port = self._server.server_address[:2]
        return str(host), int(port)

    def start(self) -> None:
        if self._server is not None:
            return
        handler = _handler_for(self._state)
        server = ThreadingHTTPServer(("127.0.0.1", self._port), handler)
        server.daemon_threads = True
        thread = threading.Thread(
            target=server.serve_forever,
            name="demo-proxy-health",
            daemon=True,
        )
        self._server = server
        self._thread = thread
        thread.start()

    def stop(self) -> None:
        server = self._server
        thread = self._thread
        if server is None:
            return
        server.shutdown()
        server.server_close()
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=2)
        self._server = None
        self._thread = None


def _handler_for(state: HealthState) -> type[BaseHTTPRequestHandler]:
    class HealthRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path == "/health":
                self._write(
                    200,
                    "application/json",
                    json.dumps(
                        state.health_payload(),
                        ensure_ascii=True,
                        separators=(",", ":"),
                        sort_keys=True,
                    ).encode("utf-8"),
                )
                return
            if self.path == "/status":
                self._write(
                    200,
                    "text/html; charset=utf-8",
                    state.status_html().encode("utf-8"),
                )
                return
            self._write(404, "application/json", b'{"error":"not found"}')

        def _write(self, status: int, content_type: str, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    return HealthRequestHandler
