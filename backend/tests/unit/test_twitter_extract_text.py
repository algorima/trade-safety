"""Unit tests for TwitterService."""

import unittest
from unittest.mock import MagicMock, patch

import requests

from trade_safety.twitter_extract_text_service import TwitterService


class TestTwitterService(unittest.TestCase):
    """Test TwitterService for tweet content fetching."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Lazy validation: token not required at initialization
        self.service = TwitterService()

    # ==============================================
    # URL Detection Tests
    # ==============================================

    def test_is_twitter_url_with_x_domain(self):
        """Test that x.com URLs are detected as Twitter URLs."""
        url = "https://x.com/mkticket7/status/2000111727493718384"

        result = TwitterService.is_twitter_url(url)

        self.assertTrue(result)

    def test_is_twitter_url_with_twitter_domain(self):
        """Test that twitter.com URLs are detected as Twitter URLs."""
        url = "https://twitter.com/user/status/123456789"

        result = TwitterService.is_twitter_url(url)

        self.assertTrue(result)

    def test_is_twitter_url_with_non_twitter_domain(self):
        """Test that non-Twitter URLs are not detected as Twitter URLs."""
        url = "https://example.com/page"

        result = TwitterService.is_twitter_url(url)

        self.assertFalse(result)

    # ==============================================
    # Tweet ID Extraction Tests
    # ==============================================

    def test_extract_tweet_id_from_x_url(self):
        """Test extracting tweet ID from x.com URL."""
        url = "https://x.com/mkticket7/status/2000111727493718384?s=20"

        tweet_id = self.service._extract_tweet_id(url)

        self.assertEqual(tweet_id, "2000111727493718384")

    def test_extract_tweet_id_from_twitter_url(self):
        """Test extracting tweet ID from twitter.com URL."""
        url = "https://twitter.com/user/status/987654321"

        tweet_id = self.service._extract_tweet_id(url)

        self.assertEqual(tweet_id, "987654321")

    def test_extract_tweet_id_with_query_params(self):
        """Test extracting tweet ID from URL with query parameters."""
        url = "https://x.com/user/status/123456789?s=20&t=abc"

        tweet_id = self.service._extract_tweet_id(url)

        self.assertEqual(tweet_id, "123456789")

    def test_extract_tweet_id_from_invalid_url(self):
        """Test that None is returned for invalid Twitter URL."""
        url = "https://x.com/user/profile"

        tweet_id = self.service._extract_tweet_id(url)

        self.assertIsNone(tweet_id)

    # ==============================================
    # API URL Building Tests
    # ==============================================

    # ==============================================
    # Tweet Text Extraction Tests
    # ==============================================

    # ==============================================
    # Integration Tests with Mocked API
    # ==============================================

    @patch('trade_safety.twitter_extract_text_service.requests.get')
    def test_fetch_tweet_content_success(self, mock_get):
        """Test fetching tweet content with mocked API response."""
        # Given: Twitter URL
        url = "https://x.com/mkticket7/status/2000111727493718384"

        # Mock API response with Twitter API v2 structure
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                'text': '2025 권진아 연말 콘서트 티켓양도\n\n12/24\n중앙블럭 1열 연석 14.5'
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # When: fetch_tweet_content is called
        result = self.service.fetch_tweet_content(url)

        # Then: tweet text should be returned
        self.assertIn('2025 권진아 연말 콘서트', result)
        self.assertIn('12/24', result)
        mock_get.assert_called_once()

    @patch('trade_safety.twitter_extract_text_service.requests.get')
    def test_fetch_tweet_content_invalid_url(self, mock_get):
        """Test that ValueError is raised for invalid Twitter URL."""
        # Given: Invalid Twitter URL (no status)
        url = "https://x.com/user/profile"

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_tweet_content(url)

        self.assertIn("Could not extract tweet ID", str(context.exception))
        mock_get.assert_not_called()

    @patch('trade_safety.twitter_extract_text_service.requests.get')
    def test_fetch_tweet_content_api_timeout(self, mock_get):
        """Test that ValueError is raised on API timeout."""
        # Given: Twitter URL
        url = "https://x.com/user/status/123456789"

        # Mock timeout
        mock_get.side_effect = requests.exceptions.Timeout()

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_tweet_content(url)

        self.assertIn("Request timeout", str(context.exception))

    @patch('trade_safety.twitter_extract_text_service.requests.get')
    def test_fetch_tweet_content_api_error(self, mock_get):
        """Test that ValueError is raised on API error."""
        # Given: Twitter URL
        url = "https://x.com/user/status/123456789"

        # Mock API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_tweet_content(url)

        self.assertIn("Failed to fetch tweet", str(context.exception))


if __name__ == "__main__":
    unittest.main()
