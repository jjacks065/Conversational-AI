"""Exact-host PAC rendering and loopback-only serving."""

from __future__ import annotations

import ipaddress
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


_HOSTNAME_PATTERN = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)"
    r"(?:\.(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?))*",
    re.IGNORECASE,
)
_TARGET_PLACEHOLDER = "__TARGET_HOST__"
_PROXY_PLACEHOLDER = "__PROXY_ENDPOINT__"


def render_pac(
    template_path: str | Path,
    *,
    target_host: str,
    proxy_host: str,
    proxy_port: int,
) -> str:
    """Render the shared PAC template using validated non-executable values."""

    normalized_target = target_host.strip().lower()
    if _HOSTNAME_PATTERN.fullmatch(normalized_target) is None:
        raise ValueError("invalid target_host for PAC file")
    try:
        address = ipaddress.ip_address(proxy_host)
    except ValueError as exc:
        raise ValueError("invalid proxy_host for PAC file") from exc
    if not address.is_loopback:
        raise ValueError("invalid proxy_host for PAC file: loopback required")
    if type(proxy_port) is not int or not 1 <= proxy_port <= 65_535:
        raise ValueError("proxy_port must be between 1 and 65535")

    template = Path(template_path).read_text(encoding="utf-8")
    if (
        template.count(_TARGET_PLACEHOLDER) != 1
        or template.count(_PROXY_PLACEHOLDER) != 1
    ):
        raise ValueError("PAC template must contain required placeholders once")
    return (
        template.replace(_TARGET_PLACEHOLDER, normalized_target)
        .replace(_PROXY_PLACEHOLDER, f"{address.compressed}:{proxy_port}")
    )


class PacServer:
    """Serve exactly one rendered PAC resource from IPv4 loopback."""

    def __init__(self, content: str, *, port: int) -> None:
        self._content = content.encode("utf-8")
        self._port = port
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def address(self) -> tuple[str, int]:
        if self._server is None:
            raise RuntimeError("PAC server is not running")
        host, port = self._server.server_address[:2]
        return str(host), int(port)

    def start(self) -> None:
        if self._server is not None:
            return
        handler = _handler_for(self._content)
        server = ThreadingHTTPServer(("127.0.0.1", self._port), handler)
        server.daemon_threads = True
        thread = threading.Thread(
            target=server.serve_forever,
            name="demo-proxy-pac",
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


def _handler_for(content: bytes) -> type[BaseHTTPRequestHandler]:
    class PacRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path != "/demo-proxy.pac":
                self._write(404, b"not found", "text/plain; charset=utf-8")
                return
            self._write(200, content, "application/x-ns-proxy-autoconfig")

        def do_HEAD(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path != "/demo-proxy.pac":
                self._write(404, b"", "text/plain; charset=utf-8", send_body=False)
                return
            self._write(
                200,
                content,
                "application/x-ns-proxy-autoconfig",
                send_body=False,
            )

        def _write(
            self,
            status: int,
            body: bytes,
            content_type: str,
            *,
            send_body: bool = True,
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if send_body:
                self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    return PacRequestHandler
