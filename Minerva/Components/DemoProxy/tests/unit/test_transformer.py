from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from proxy.transformer import transform_content, transform_payload


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FIXTURE_PATH = PROJECT_ROOT / "Content-Sample.JSON"
OUTPUT_FIXTURE_PATH = PROJECT_ROOT / "Content-Sample-Output.JSON"

# Expected transformation marker (invisible span at end)
TRANSFORM_MARKER = '<span style="display:none;" data-transformed="true"></span>'


class TransformContentTests(unittest.TestCase):
    def test_rejects_non_string_content(self) -> None:
        with self.assertRaisesRegex(TypeError, "content must be a string"):
            transform_content(None)  # type: ignore[arg-type]

    def test_converts_h3_markdown_to_html_with_inline_styles(self) -> None:
        content = "### A. Test Header"
        result = transform_content(content)
        
        self.assertIn(TRANSFORM_MARKER, result)
        self.assertIn('<h3 style="', result)
        self.assertIn('A. Test Header</h3>', result)
        self.assertNotIn('###', result)

    def test_converts_h4_markdown_to_html_with_inline_styles(self) -> None:
        content = "#### In-Network Provider"
        result = transform_content(content)
        
        self.assertIn('<h4 style="', result)
        self.assertIn('In-Network Provider</h4>', result)

    def test_converts_h2_markdown_to_html_with_inline_styles(self) -> None:
        content = "## Main Section"
        result = transform_content(content)
        
        self.assertIn('<h2 style="', result)
        self.assertIn('Main Section</h2>', result)

    def test_preserves_non_header_content(self) -> None:
        content = "Regular paragraph text\n\nAnother paragraph"
        result = transform_content(content)
        
        self.assertIn("Regular paragraph text", result)
        self.assertIn("Another paragraph", result)

    def test_preserves_hyphens_inside_markdown_tables_and_prose(self) -> None:
        content = "| Ref | Source |\n|-----|--------|\nvalue---suffix"
        result = transform_content(content)
        
        self.assertIn("| Ref | Source |", result)
        self.assertIn("|-----|--------|", result)
        self.assertIn("value---suffix", result)

    def test_preserves_crlf_and_cr_line_endings(self) -> None:
        """Line ending normalization removed - transformation only."""
        content = "alpha\r\n\r\nbeta\rgamma\r\ndelta"
        result = transform_content(content)
        
        self.assertIn("alpha\r\n\r\nbeta\rgamma\r\ndelta", result)

    def test_handles_multiple_headers(self) -> None:
        content = "### First\n\nSome text\n\n#### Second\n\nMore text\n\n### Third"
        result = transform_content(content)
        
        self.assertEqual(result.count('<h3'), 2)
        self.assertEqual(result.count('<h4'), 1)
        self.assertIn('First</h3>', result)
        self.assertIn('Second</h4>', result)
        self.assertIn('Third</h3>', result)

    def test_preserves_fenced_content(self) -> None:
        content = "```text\nalpha\n\nbeta\n---\n```"
        result = transform_content(content)
        
        self.assertIn("```text", result)

    def test_is_idempotent(self) -> None:
        content = "### Test Header\n\nSome content"
        transformed = transform_content(content)

        # Applying transform again should not transform again
        self.assertEqual(transform_content(transformed), transformed)

    def test_preserves_unicode(self) -> None:
        input_text = "### café\n\nplan's\n— covered"
        result = transform_content(input_text)
        
        self.assertIn("café", result)
        self.assertIn("plan's", result)
        self.assertIn("— covered", result)


class TransformPayloadTests(unittest.TestCase):
    def test_transforms_only_content_and_does_not_mutate_input(self) -> None:
        payload = {
            "questionId": "question-1",
            "sessionId": "session-1",
            "content": "### Header\n\nalpha\n\nbeta",
            "responseId": "response-1",
            "unknown": {"nested": [1, 2, 3]},
        }
        original = copy.deepcopy(payload)

        transformed = transform_payload(payload)

        self.assertEqual(payload, original)
        # Content should be transformed
        self.assertIn(TRANSFORM_MARKER, transformed["content"])
        self.assertIn("<h3", transformed["content"])
        self.assertEqual(transformed["unknown"], payload["unknown"])
        self.assertIsNot(transformed, payload)
        self.assertIsNot(transformed["unknown"], payload["unknown"])

    def test_missing_or_non_string_content_is_returned_unchanged(self) -> None:
        for payload in ({"responseId": "response-1"}, {"content": None}):
            with self.subTest(payload=payload):
                self.assertEqual(transform_payload(payload), payload)

    def test_rejects_non_mapping_payload(self) -> None:
        with self.assertRaisesRegex(TypeError, "payload must be a dict"):
            transform_payload(["not", "a", "dict"])  # type: ignore[arg-type]

    def test_payload_transform_is_idempotent(self) -> None:
        payload = {
            "content": "### Header\n\nalpha",
            "unknown": {"nested": True},
        }

        transformed = transform_payload(payload)

        self.assertEqual(transform_payload(transformed), transformed)

    def test_preserves_protected_and_unknown_fields_exactly(self) -> None:
        payload = {
            "content": "alpha\n\nbeta",
            "questionId": "question-1",
            "sessionId": "session-1",
            "responseId": "response-1",
            "tool_calls": [
                {"function": {"name": "lookup", "arguments": {"plan": "A-1"}}}
            ],
            "authentication": {"scope": "read"},
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "billing": {"units": 30},
            "unknown": {"nested": [None, True, 3.14]},
        }

        transformed = transform_payload(payload)

        for field in (
            "questionId",
            "sessionId",
            "responseId",
            "tool_calls",
            "authentication",
            "usage",
            "billing",
            "unknown",
        ):
            with self.subTest(field=field):
                self.assertEqual(transformed[field], payload[field])
        # Content should have marker but no headers to transform
        self.assertIn(TRANSFORM_MARKER, transformed["content"])
        self.assertIn("alpha", transformed["content"])
        self.assertIn("beta", transformed["content"])

    def test_input_fixture_matches_expected_output_fixture_exactly(self) -> None:
        payload = json.loads(INPUT_FIXTURE_PATH.read_text(encoding="utf-8"))
        expected = json.loads(OUTPUT_FIXTURE_PATH.read_text(encoding="utf-8"))

        transformed = transform_payload(payload)

        # All fields should match except content which is transformed
        self.assertEqual(transformed["questionId"], expected["questionId"])
        self.assertEqual(transformed["sessionId"], expected["sessionId"])
        self.assertEqual(transformed["responseId"], expected["responseId"])
        # Content should have marker and transformed headers
        self.assertIn(TRANSFORM_MARKER, transformed["content"])
        # Should have at least some h3 tags from the markdown headers
        self.assertIn("<h3", transformed["content"])


if __name__ == "__main__":
    unittest.main()
