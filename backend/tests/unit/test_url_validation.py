"""Unit tests for TradeSafetyService URL validation."""

import unittest

from aioia_core.settings import OpenAIAPISettings

from trade_safety.service import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings, TwitterAPISettings


class TestURLValidation(unittest.TestCase):
    """Test _is_url method for URL detection."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        openai_api = OpenAIAPISettings(api_key="sk-test-dummy-key")
        model_settings = TradeSafetyModelSettings()
        twitter_api = TwitterAPISettings(bearer_token="test-dummy-twitter-token")
        self.service = TradeSafetyService(openai_api, model_settings, twitter_api=twitter_api)

    # ==============================================
    # URLs - Should Return True
    # ==============================================

    def test_detect_https_url(self):
        """Test that HTTPS URL returns True."""
        url = "https://go.bgzt.link/7f2qhi"

        result = self.service._is_url(url)

        self.assertTrue(result)

    def test_detect_http_url(self):
        """Test that HTTP URL returns True."""
        url = "http://example.com/trade"

        result = self.service._is_url(url)

        self.assertTrue(result)

    def test_detect_twitter_url(self):
        """Test that Twitter/X URL returns True."""
        url = "https://x.com/mkticket7/status/2000111727493718384?s=20"

        result = self.service._is_url(url)

        self.assertTrue(result)

    def test_detect_url_with_path_and_query(self):
        """Test that URL with path and query parameters returns True."""
        url = "https://cafe.naver.com/ArticleRead.nhn?clubid=123&articleid=456"

        result = self.service._is_url(url)

        self.assertTrue(result)

    def test_detect_url_with_subdomain(self):
        """Test that URL with subdomain returns True."""
        url = "https://www.bunjang.co.kr/products/12345"

        result = self.service._is_url(url)

        self.assertTrue(result)

    def test_detect_url_with_whitespace(self):
        """Test that URL with leading/trailing whitespace returns True."""
        url = "  https://go.bgzt.link/7f2qhi  "

        result = self.service._is_url(url)

        self.assertTrue(result)

    # ==============================================
    # Non-URLs - Should Return False
    # ==============================================

    def test_korean_text_is_not_url(self):
        """Test that Korean trade post text returns False."""
        text = "급처분 ㅠㅠ 공구 실패해서 양도해요"

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_text_with_price_is_not_url(self):
        """Test that trade post with price returns False."""
        text = "포카 양도합니다 20,000원"

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_multiline_text_is_not_url(self):
        """Test that multiline trade post text returns False."""
        text = """
        [양도] BTS 포카
        가격: 15,000원
        상태: 미개봉
        """

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_empty_string_is_not_url(self):
        """Test that empty string returns False."""
        text = ""

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_text_containing_http_word_is_not_url(self):
        """Test that text containing 'http' word returns False."""
        text = "http로 시작하는 주소는 안전하지 않아요"

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_url_like_pattern_is_not_url(self):
        """Test that URL-like pattern without domain returns False."""
        text = "https://로 시작"

        result = self.service._is_url(text)

        self.assertTrue(result)

    def test_text_with_embedded_url_is_not_url(self):
        """Test that trade post text with embedded URL returns False."""
        text = "양도합니다! 자세한 내용은 https://example.com 참고하세요"

        result = self.service._is_url(text)

        # Text starting with Korean, URL embedded
        # Should return False (doesn't start with http/https)
        self.assertFalse(result)

    # ==============================================
    # Edge Cases
    # ==============================================

    def test_malformed_url_is_not_url(self):
        """Test that malformed URL (missing domain) returns False."""
        text = "https://"

        result = self.service._is_url(text)

        self.assertFalse(result)

    def test_ftp_url_is_not_detected(self):
        """Test that FTP URL (non-HTTP scheme) returns False."""
        url = "ftp://example.com/file.txt"

        result = self.service._is_url(url)

        # FTP should return False (only http/https are detected)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()