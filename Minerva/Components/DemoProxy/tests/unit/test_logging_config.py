from __future__ import annotations

import json
import logging
import unittest

from proxy.logging_config import EVENT_FIELDS, StructuredLogger


class RecordingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


class StructuredLoggingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = RecordingHandler()
        self.logger = logging.getLogger(f"demo-proxy-test-{id(self)}")
        self.logger.handlers = [self.handler]
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.structured = StructuredLogger(
            level="INFO",
            platform_label="test-platform",
            proxy_version="0.1.0",
            logger=self.logger,
        )

    def test_emits_only_allowlisted_metadata_as_json(self) -> None:
        self.structured.emit(
            correlation_id="flow-1",
            match_result="matched",
            method="POST",
            host="api.example.com",
            path_template=r"^/api/chatbot/ask$",
            status_code=200,
            content_type="application/json",
            transformation_duration_ms=1.25,
            original_bytes=100,
            transformed_bytes=120,
            fail_open=False,
            exception_category=None,
        )

        event = json.loads(self.handler.messages[-1])
        self.assertEqual(set(event), EVENT_FIELDS)
        self.assertEqual(event["platform"], "test-platform")
        self.assertEqual(event["proxy_version"], "0.1.0")
        self.assertEqual(event["match_result"], "matched")
        self.assertNotIn("request_body", event)
        self.assertNotIn("response_body", event)
        self.assertNotIn("headers", event)

    def test_sensitive_values_cannot_be_passed_as_extra_fields(self) -> None:
        with self.assertRaisesRegex(TypeError, "unexpected keyword"):
            self.structured.emit(  # type: ignore[call-arg]
                correlation_id="flow-1",
                match_result="matched",
                method="POST",
                host="api.example.com",
                path_template=r"^/api/chatbot/ask$",
                status_code=200,
                content_type="application/json",
                transformation_duration_ms=1.0,
                original_bytes=100,
                transformed_bytes=100,
                fail_open=False,
                exception_category=None,
                authorization="Bearer secret-token",
            )


if __name__ == "__main__":
    unittest.main()
