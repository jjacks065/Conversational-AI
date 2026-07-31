"""Native runtime smoke test without certificate-store or startup-service mutation."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any


def smoke_proxy_runtime(
    *, runtime_path: Path, source_root: Path, timeout_seconds: float = 20
) -> dict[str, Any]:
    ports = _free_ports(3)
    proxy_port, health_port, pac_port = ports
    with tempfile.TemporaryDirectory(prefix="demo-proxy-package-smoke-") as temporary:
        root = Path(temporary)
        config_path = root / "proxy.yaml"
        config = (source_root / "config" / "proxy.example.yaml").read_text(
            encoding="utf-8"
        )
        config = config.replace("listen_port: 8080", f"listen_port: {proxy_port}")
        config = config.replace("health_port: 8081", f"health_port: {health_port}")
        config = config.replace("pac_port: 8765", f"pac_port: {pac_port}")
        config_path.write_text(config, encoding="utf-8", newline="\n")
        confdir = root / "mitmproxy"
        environment = {
            **os.environ,
            "DEMO_PROXY_CERTIFICATE_TRUSTED": "false",
            "DEMO_PROXY_PLATFORM": "package-smoke",
            "PYTHONPATH": str(source_root),
        }
        process = subprocess.Popen(
            [
                str(runtime_path),
                "--listen-host",
                "127.0.0.1",
                "--listen-port",
                str(proxy_port),
                "--set",
                f"confdir={confdir}",
                "--set",
                "flow_detail=0",
                "--set",
                f"demo_proxy_config={config_path}",
                "--scripts",
                str(source_root / "proxy" / "addon.py"),
            ],
            cwd=source_root,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        smoke_succeeded = False
        try:
            health = _wait_json(
                f"http://127.0.0.1:{health_port}/health",
                process=process,
                timeout_seconds=timeout_seconds,
            )
            pac = _read_url(f"http://127.0.0.1:{pac_port}/demo-proxy.pac")
            if not health.get("proxyListening") or not health.get("pacServerListening"):
                raise RuntimeError(f"packaged runtime reported incomplete health: {health}")
            if "api.demo.example.com" not in pac or "FindProxyForURL" not in pac:
                raise RuntimeError("packaged runtime PAC response is incomplete")
            if not (confdir / "mitmproxy-ca-cert.cer").is_file():
                raise RuntimeError("packaged runtime did not generate a local CA")
            smoke_succeeded = True
            return {
                "healthPort": health_port,
                "pacPort": pac_port,
                "proxyPort": proxy_port,
                "status": "passed",
            }
        finally:
            process_was_running = process.poll() is None
            if process_was_running:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            stdout, stderr = process.communicate()
            if smoke_succeeded and not process_was_running:
                raise RuntimeError(
                    f"packaged runtime exited immediately after smoke validation: "
                    f"{stderr.strip() or stdout.strip()}"
                )
            if not smoke_succeeded and process.returncode not in {0, -15, 15}:
                raise RuntimeError(
                    f"packaged runtime exited with {process.returncode}: "
                    f"{stderr.strip() or stdout.strip()}"
                )


def _free_ports(count: int) -> list[int]:
    listeners: list[socket.socket] = []
    try:
        for _ in range(count):
            listener = socket.socket()
            listener.bind(("127.0.0.1", 0))
            listeners.append(listener)
        return [int(listener.getsockname()[1]) for listener in listeners]
    finally:
        for listener in listeners:
            listener.close()


def _wait_json(
    url: str, *, process: subprocess.Popen[str], timeout_seconds: float
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            raise RuntimeError(
                f"packaged runtime exited before health startup: "
                f"{stderr.strip() or stdout.strip()}"
            )
        try:
            return json.loads(_read_url(url))
        except Exception as exc:  # noqa: BLE001 - retry all connection/parse failures
            last_error = exc
            time.sleep(0.1)
    raise RuntimeError(f"timed out waiting for packaged runtime health: {last_error}")


def _read_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=2) as response:
        return response.read().decode("utf-8")
