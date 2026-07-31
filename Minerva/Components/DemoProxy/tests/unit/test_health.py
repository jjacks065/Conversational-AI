from __future__ import annotations

import json
import unittest
import urllib.error
import urllib.request

from proxy.health import HealthServer, HealthState


class HealthStateTests(unittest.TestCase):
    def test_health_and_status_contain_metadata_only(self) -> None:
        state = HealthState(
            platform_label="test-platform",
            target_host="api.example.com",
            transformer_version="1.0.0",
            fail_open=True,
        )
        state.set_configuration_loaded(True)
        state.set_proxy_listening(True)
        state.set_pac_server_listening(True)
        state.set_certificate_trusted(True)
        state.record_match()
        state.record_transformation(success=True)

        payload = state.health_payload()
        page = state.status_html()

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["platform"], "test-platform")
        self.assertTrue(payload["proxyListening"])
        self.assertEqual(payload["targetHost"], "api.example.com")
        self.assertIn("Last transformation: Successful", page)
        for sensitive in ("prompt", "response text", "token", "cookie", "credential"):
            self.assertNotIn(sensitive, page.lower())

    def test_health_is_degraded_until_all_operator_dependencies_are_ready(self) -> None:
        state = HealthState(
            platform_label="test-platform",
            target_host="api.example.com",
            transformer_version="1.0.0",
            fail_open=True,
        )
        state.set_configuration_loaded(True)
        state.set_proxy_listening(True)

        self.assertEqual(state.health_payload()["status"], "degraded")


class HealthServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = HealthState(
            platform_label="test-platform",
            target_host="api.example.com",
            transformer_version="1.0.0",
            fail_open=True,
        )
        self.state.set_configuration_loaded(True)
        self.server = HealthServer(self.state, port=0)
        self.server.start()
        self.addCleanup(self.server.stop)

    def test_serves_health_json_and_operator_status_on_loopback(self) -> None:
        host, port = self.server.address
        self.assertEqual(host, "127.0.0.1")

        with urllib.request.urlopen(f"http://{host}:{port}/health", timeout=2) as response:
            payload = json.loads(response.read())
            self.assertEqual(response.headers["Content-Type"], "application/json")
        with urllib.request.urlopen(f"http://{host}:{port}/status", timeout=2) as response:
            page = response.read().decode("utf-8")
            self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")

        self.assertEqual(payload["targetHost"], "api.example.com")
        self.assertIn("Demo Response Proxy", page)

    def test_unknown_path_returns_404_without_state_details(self) -> None:
        host, port = self.server.address

        with self.assertRaises(urllib.error.HTTPError) as raised:
            urllib.request.urlopen(f"http://{host}:{port}/missing", timeout=2)

        self.assertEqual(raised.exception.code, 404)
        self.assertEqual(json.loads(raised.exception.read()), {"error": "not found"})
        raised.exception.close()

    def test_start_and_stop_are_idempotent(self) -> None:
        self.server.start()
        self.server.stop()
        self.server.stop()


if __name__ == "__main__":
    unittest.main()
