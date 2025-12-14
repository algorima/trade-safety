"""Unit tests for TradeSafetyCheckRequest API schema."""

import unittest

from pydantic import ValidationError

from trade_safety.api.router import TradeSafetyCheckRequest


class TestTradeSafetyCheckRequest(unittest.TestCase):
    """Test TradeSafetyCheckRequest schema with output_language field."""

    def test_request_with_default_output_language(self):
        """Test that output_language defaults to 'en' when not provided."""
        request = TradeSafetyCheckRequest(input_text="[WTS] K-pop goods for sale")
        self.assertEqual(request.output_language, "en")

    def test_request_with_korean_output_language(self):
        """Test that output_language can be set to 'ko' (Korean)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="ko"
        )
        self.assertEqual(request.output_language, "ko")

    def test_request_with_spanish_output_language(self):
        """Test that output_language can be set to 'es' (Spanish)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="es"
        )
        self.assertEqual(request.output_language, "es")

    def test_request_with_indonesian_output_language(self):
        """Test that output_language can be set to 'id' (Indonesian)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="id"
        )
        self.assertEqual(request.output_language, "id")

    def test_request_with_japanese_output_language(self):
        """Test that output_language can be set to 'ja' (Japanese)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="ja"
        )
        self.assertEqual(request.output_language, "ja")

    def test_request_with_chinese_output_language(self):
        """Test that output_language can be set to 'zh' (Chinese)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="zh"
        )
        self.assertEqual(request.output_language, "zh")

    def test_request_with_thai_output_language(self):
        """Test that output_language can be set to 'th' (Thai)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="th"
        )
        self.assertEqual(request.output_language, "th")

    def test_request_with_vietnamese_output_language(self):
        """Test that output_language can be set to 'vi' (Vietnamese)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="vi"
        )
        self.assertEqual(request.output_language, "vi")

    def test_request_with_tagalog_output_language(self):
        """Test that output_language can be set to 'tl' (Tagalog/Filipino)."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="tl"
        )
        self.assertEqual(request.output_language, "tl")

    def test_request_with_url_input(self):
        """Test that input_text accepts URL format."""
        request = TradeSafetyCheckRequest(
            input_text="https://www.reddit.com/", output_language="en"
        )
        self.assertEqual(request.input_text, "https://www.reddit.com/")
        self.assertEqual(request.output_language, "en")

    def test_request_with_url_and_korean_language(self):
        """Test that URL input works with Korean output language."""
        request = TradeSafetyCheckRequest(
            input_text="https://www.reddit.com/", output_language="ko"
        )
        self.assertEqual(request.input_text, "https://www.reddit.com/")
        self.assertEqual(request.output_language, "ko")

    def test_request_requires_input_text(self):
        """Test that input_text is a required field."""
        with self.assertRaises(ValidationError) as context:
            TradeSafetyCheckRequest()  # type: ignore[call-arg]

        error = context.exception
        error_fields = [e["loc"][0] for e in error.errors()]
        self.assertIn("input_text", error_fields)

    def test_request_serialization_includes_output_language(self):
        """Test that serialized request includes output_language field."""
        request = TradeSafetyCheckRequest(
            input_text="[WTS] K-pop goods for sale", output_language="ko"
        )
        data = request.model_dump()
        self.assertIn("output_language", data)
        self.assertEqual(data["output_language"], "ko")
        self.assertEqual(data["input_text"], "[WTS] K-pop goods for sale")


if __name__ == "__main__":
    unittest.main()
