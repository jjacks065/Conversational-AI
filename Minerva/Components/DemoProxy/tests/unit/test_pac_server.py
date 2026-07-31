from __future__ import annotations

import unittest
import urllib.error
import urllib.request
import json
import shutil
import subprocess
from pathlib import Path

from proxy.pac_server import PacServer, render_pac


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = PROJECT_ROOT / "pac" / "demo-proxy.pac"


class PacRenderingTests(unittest.TestCase):
    def test_renders_exact_host_proxy_rule_with_direct_fallback(self) -> None:
        content = render_pac(
            TEMPLATE_PATH,
            target_host="api.example.com",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )

        self.assertIn('normalizedHost === "api.example.com"', content)
        self.assertIn('return "PROXY 127.0.0.1:8080; DIRECT"', content)
        self.assertIn('return "DIRECT"', content)
        self.assertNotIn("dnsDomainIs", content)
        self.assertNotIn("__TARGET_HOST__", content)
        self.assertNotIn("__PROXY_ENDPOINT__", content)

    def test_rejects_values_that_could_inject_javascript(self) -> None:
        for target_host, proxy_host in (
            ('api.example.com";alert(1)//', "127.0.0.1"),
            ("api.example.com", "127.0.0.1; DIRECT"),
        ):
            with self.subTest(target_host=target_host, proxy_host=proxy_host):
                with self.assertRaisesRegex(ValueError, "invalid"):
                    render_pac(
                        TEMPLATE_PATH,
                        target_host=target_host,
                        proxy_host=proxy_host,
                        proxy_port=8080,
                    )

        with self.assertRaisesRegex(ValueError, "loopback"):
            render_pac(
                TEMPLATE_PATH,
                target_host="api.example.com",
                proxy_host="192.0.2.1",
                proxy_port=8080,
            )

    def test_rejects_invalid_proxy_port_or_template(self) -> None:
        with self.assertRaisesRegex(ValueError, "proxy_port"):
            render_pac(
                TEMPLATE_PATH,
                target_host="api.example.com",
                proxy_host="127.0.0.1",
                proxy_port=70_000,
            )

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_pac_runtime_routes_only_exact_target_host(self) -> None:
        content = render_pac(
            TEMPLATE_PATH,
            target_host="api.example.com",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )
        script = (
            content
            + "\nconsole.log(JSON.stringify(["
            + "FindProxyForURL('https://api.example.com/x','api.example.com'),"
            + "FindProxyForURL('https://API.EXAMPLE.COM/x','API.EXAMPLE.COM'),"
            + "FindProxyForURL('https://api.example.com.attacker.test/x','api.example.com.attacker.test'),"
            + "FindProxyForURL('https://nexus.example.com/x','nexus.example.com')"
            + "]));"
        )

        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            [
                "PROXY 127.0.0.1:8080; DIRECT",
                "PROXY 127.0.0.1:8080; DIRECT",
                "DIRECT",
                "DIRECT",
            ],
        )
        with self.assertRaisesRegex(ValueError, "placeholders"):
            render_pac(
                PROJECT_ROOT / "Content-Sample.md",
                target_host="api.example.com",
                proxy_host="127.0.0.1",
                proxy_port=8080,
            )


class PacServerTests(unittest.TestCase):
    def setUp(self) -> None:
        content = render_pac(
            TEMPLATE_PATH,
            target_host="api.example.com",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )
        self.server = PacServer(content, port=0)
        self.server.start()
        self.addCleanup(self.server.stop)

    def test_serves_only_pac_file_on_ipv4_loopback(self) -> None:
        host, port = self.server.address
        self.assertEqual(host, "127.0.0.1")

        with urllib.request.urlopen(
            f"http://{host}:{port}/demo-proxy.pac", timeout=2
        ) as response:
            body = response.read().decode("utf-8")

        self.assertEqual(
            response.headers["Content-Type"],
            "application/x-ns-proxy-autoconfig",
        )
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertIn("FindProxyForURL", body)

    def test_head_reports_pac_metadata_without_body(self) -> None:
        host, port = self.server.address
        request = urllib.request.Request(
            f"http://{host}:{port}/demo-proxy.pac", method="HEAD"
        )

        with urllib.request.urlopen(request, timeout=2) as response:
            body = response.read()

        self.assertEqual(response.status, 200)
        self.assertEqual(body, b"")
        self.assertGreater(int(response.headers["Content-Length"]), 0)

        missing = urllib.request.Request(f"http://{host}:{port}/missing", method="HEAD")
        with self.assertRaises(urllib.error.HTTPError) as raised:
            urllib.request.urlopen(missing, timeout=2)
        self.assertEqual(raised.exception.code, 404)
        raised.exception.close()

    def test_rejects_all_other_paths(self) -> None:
        host, port = self.server.address
        for path in ("/", "/demo-proxy.pac/extra", "/../config/proxy.yaml"):
            with self.subTest(path=path):
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    urllib.request.urlopen(f"http://{host}:{port}{path}", timeout=2)
                self.assertEqual(raised.exception.code, 404)
                raised.exception.close()

    def test_start_and_stop_are_idempotent(self) -> None:
        self.server.start()
        self.server.stop()
        self.server.stop()

    def test_address_requires_running_server(self) -> None:
        server = PacServer("function FindProxyForURL(){return 'DIRECT';}", port=0)

        with self.assertRaisesRegex(RuntimeError, "not running"):
            _ = server.address


if __name__ == "__main__":
    unittest.main()
