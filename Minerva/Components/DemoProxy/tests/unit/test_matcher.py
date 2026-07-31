from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path

from proxy.config import load_config, parse_config
from proxy.matcher import RequestMetadata, ResponseMatcher, ResponseMetadata
from tests.unit.test_config import valid_config_mapping


class MatcherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = parse_config(valid_config_mapping())
        self.matcher = ResponseMatcher(self.config)
        self.request = RequestMetadata(
            scheme="https",
            host="api.example.com",
            port=443,
            method="POST",
            path="/api/chatbot/ask",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Origin": "https://demo.example.com",
            },
        )
        self.response = ResponseMetadata(
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

    def test_matches_all_confirmed_conditions(self) -> None:
        decision = self.matcher.evaluate(self.request, self.response)

        self.assertTrue(decision.matched)
        self.assertEqual(decision.reason, "matched")
        self.assertEqual(decision.path_pattern, r"^/api/chatbot/ask$")

    def test_query_string_does_not_change_path_match(self) -> None:
        request = replace(self.request, path="/api/chatbot/ask?trace=safe")

        self.assertTrue(self.matcher.evaluate(request, self.response).matched)

    def test_rejects_each_nonmatching_request_dimension(self) -> None:
        cases = {
            "scheme": replace(self.request, scheme="http"),
            "host": replace(self.request, host="api.example.com.attacker.test"),
            "port": replace(self.request, port=8443),
            "method": replace(self.request, method="GET"),
            "path": replace(self.request, path="/api/chatbot/ask/extra"),
            "request_content_type": replace(
                self.request,
                headers={**self.request.headers, "Content-Type": "text/plain"},
            ),
        }

        for reason, request in cases.items():
            with self.subTest(reason=reason):
                decision = self.matcher.evaluate(request, self.response)
                self.assertFalse(decision.matched)
                self.assertEqual(decision.reason, reason)

    def test_host_and_header_names_are_case_insensitive(self) -> None:
        request = replace(
            self.request,
            host="API.EXAMPLE.COM",
            headers={
                "content-type": "application/json",
                "ORIGIN": "https://demo.example.com",
            },
        )

        self.assertTrue(self.matcher.evaluate(request, self.response).matched)

    def test_rejects_missing_or_invalid_marker_header(self) -> None:
        missing = replace(
            self.request,
            headers={"Content-Type": "application/json"},
        )
        invalid = replace(
            self.request,
            headers={
                "Content-Type": "application/json",
                "Origin": "https://not-demo.example.com",
            },
        )

        self.assertEqual(
            self.matcher.evaluate(missing, self.response).reason,
            "required_header_missing",
        )
        self.assertEqual(
            self.matcher.evaluate(invalid, self.response).reason,
            "required_header_mismatch",
        )

    def test_rejects_response_content_type(self) -> None:
        response = ResponseMetadata(headers={"Content-Type": "text/event-stream"})

        decision = self.matcher.evaluate(self.request, response)

        self.assertFalse(decision.matched)
        self.assertEqual(decision.reason, "response_content_type")

    def test_rejects_missing_content_types(self) -> None:
        request = replace(self.request, headers={"Origin": "https://demo.example.com"})
        response = ResponseMetadata(headers={})

        self.assertEqual(
            self.matcher.evaluate(request, self.response).reason,
            "request_content_type",
        )
        self.assertEqual(
            self.matcher.evaluate(self.request, response).reason,
            "response_content_type",
        )

    def test_disabled_transformation_never_matches(self) -> None:
        source = valid_config_mapping()
        source["transformation"]["enabled"] = False  # type: ignore[index]
        matcher = ResponseMatcher(parse_config(source))

        decision = matcher.evaluate(self.request, self.response)

        self.assertFalse(decision.matched)
        self.assertEqual(decision.reason, "transformation_disabled")

    def test_real_configuration_matches_confirmed_protocol(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        matcher = ResponseMatcher(load_config(project_root / "config" / "proxy.yaml"))
        request = RequestMetadata(
            scheme="https",
            host="app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net",
            port=443,
            method="POST",
            path="/api/chatbot/ask",
            headers={
                "Content-Type": "application/json",
                "Origin": "https://nexus-cloud-web-stg.bsc.bscal.com",
            },
        )

        decision = matcher.evaluate(
            request,
            ResponseMetadata(headers={"Content-Type": "application/json; charset=utf-8"}),
        )

        self.assertTrue(decision.matched)


if __name__ == "__main__":
    unittest.main()
