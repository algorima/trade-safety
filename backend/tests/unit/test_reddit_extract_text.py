"""Unit tests for RedditService."""

import unittest
from unittest.mock import patch, MagicMock

from trade_safety.reddit_extract_text_service import RedditService


class TestRedditService(unittest.TestCase):
    """Test RedditService for Reddit post content fetching."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = RedditService()

    # ==============================================
    # URL Detection Tests
    # ==============================================

    def test_is_reddit_url_with_www(self):
        """Test that www.reddit.com URLs are detected as Reddit URLs."""
        url = "https://www.reddit.com/r/mildlyinfuriating/comments/1pog0er/title"

        result = RedditService.is_reddit_url(url)

        self.assertTrue(result)

    def test_is_reddit_url_without_www(self):
        """Test that reddit.com URLs without www are detected as Reddit URLs."""
        url = "https://reddit.com/r/test/comments/123/title"

        result = RedditService.is_reddit_url(url)

        self.assertTrue(result)

    def test_is_reddit_url_with_non_reddit_domain(self):
        """Test that non-Reddit URLs are not detected as Reddit URLs."""
        url = "https://example.com/page"

        result = RedditService.is_reddit_url(url)

        self.assertFalse(result)

    # ==============================================
    # Post ID Extraction Tests
    # ==============================================

    def test_extract_post_id_from_standard_url(self):
        """Test extracting post ID from standard Reddit URL."""
        url = "https://www.reddit.com/r/mildlyinfuriating/comments/1pog0er/got_screwed_over"

        post_id = RedditService.extract_post_id(url)

        self.assertEqual(post_id, "1pog0er")

    def test_extract_post_id_from_url_with_full_title(self):
        """Test extracting post ID from URL with full title."""
        url = "https://www.reddit.com/r/test/comments/abc123/this_is_a_long_title_here"

        post_id = RedditService.extract_post_id(url)

        self.assertEqual(post_id, "abc123")

    def test_extract_post_id_from_url_without_title(self):
        """Test extracting post ID from URL without title."""
        url = "https://www.reddit.com/r/test/comments/xyz789/"

        post_id = RedditService.extract_post_id(url)

        self.assertEqual(post_id, "xyz789")

    def test_extract_post_id_from_invalid_url(self):
        """Test that None is returned for invalid Reddit URL."""
        url = "https://www.reddit.com/r/subreddit/"

        post_id = RedditService.extract_post_id(url)

        self.assertIsNone(post_id)

    # ==============================================
    # JSON URL Conversion Tests
    # ==============================================

    def test_convert_to_json_url_basic(self):
        """Test converting basic Reddit URL to JSON URL."""
        url = "https://www.reddit.com/r/test/comments/123/title"

        json_url = self.service._convert_to_json_url(url)

        self.assertEqual(json_url, "https://www.reddit.com/r/test/comments/123/title.json")

    def test_convert_to_json_url_with_trailing_slash(self):
        """Test converting Reddit URL with trailing slash to JSON URL."""
        url = "https://www.reddit.com/r/test/comments/123/title/"

        json_url = self.service._convert_to_json_url(url)

        self.assertEqual(json_url, "https://www.reddit.com/r/test/comments/123/title.json")

    def test_convert_to_json_url_already_has_json(self):
        """Test that URL already ending with .json is not modified."""
        url = "https://www.reddit.com/r/test/comments/123/title.json"

        json_url = self.service._convert_to_json_url(url)

        self.assertEqual(json_url, url)

    # ==============================================
    # Selftext Extraction Tests
    # ==============================================

    def test_extract_selftext_from_standard_response(self):
        """Test extracting selftext from standard Reddit JSON response."""
        json_data = [
            {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t3",
                            "data": {
                                "selftext": "This is the post content.",
                                "title": "Test Post"
                            }
                        }
                    ]
                }
            }
        ]

        selftext = self.service._extract_selftext(json_data)

        self.assertEqual(selftext, "This is the post content.")

    def test_extract_selftext_with_long_content(self):
        """Test extracting selftext with long multi-line content."""
        long_text = (
            "So last night I was at at Christmas party where everyone was asked to bring "
            "a wrapped $25 white elephant gift for exchange.\n\n"
            "White elephant gifts are often meant to be silly, but in this group we usually "
            "get cool/practical/random things that are actually useful."
        )

        json_data = [
            {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t3",
                            "data": {
                                "selftext": long_text
                            }
                        }
                    ]
                }
            }
        ]

        selftext = self.service._extract_selftext(json_data)

        self.assertEqual(selftext, long_text)
        self.assertIn("Christmas party", selftext)
        self.assertIn("white elephant", selftext)

    def test_extract_selftext_empty_selftext(self):
        """Test that None is returned when selftext is empty."""
        json_data = [
            {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t3",
                            "data": {
                                "selftext": ""
                            }
                        }
                    ]
                }
            }
        ]

        selftext = self.service._extract_selftext(json_data)

        self.assertIsNone(selftext)

    def test_extract_selftext_missing_data(self):
        """Test that None is returned when data structure is incomplete."""
        json_data = [
            {
                "kind": "Listing",
                "data": {
                    "children": []
                }
            }
        ]

        selftext = self.service._extract_selftext(json_data)

        self.assertIsNone(selftext)

    def test_extract_selftext_invalid_structure(self):
        """Test that None is returned for invalid JSON structure."""
        json_data = {"invalid": "structure"}

        selftext = self.service._extract_selftext(json_data)

        self.assertIsNone(selftext)

    def test_extract_selftext_none_input(self):
        """Test that None is returned when input is None."""
        selftext = self.service._extract_selftext(None)

        self.assertIsNone(selftext)

    # ==============================================
    # Integration Tests with Mocked API
    # ==============================================

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_success(self, mock_get):
        """Test fetching post content with mocked API response."""
        # Given: Reddit URL
        url = "https://www.reddit.com/r/test/comments/123/title"

        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t3",
                            "data": {
                                "selftext": "This is a test post content.",
                                "title": "Test Post"
                            }
                        }
                    ]
                }
            }
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # When: fetch_post_content is called
        result = self.service.fetch_post_content(url)

        # Then: post content should be returned
        self.assertEqual(result, "This is a test post content.")
        mock_get.assert_called_once()

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_invalid_url(self, mock_get):
        """Test that ValueError is raised for invalid Reddit URL."""
        # Given: Invalid Reddit URL (not a reddit.com domain)
        url = "https://example.com/post"

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_post_content(url)

        self.assertIn("Invalid Reddit URL", str(context.exception))
        mock_get.assert_not_called()

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_no_selftext(self, mock_get):
        """Test that ValueError is raised when post has no selftext."""
        # Given: Reddit URL
        url = "https://www.reddit.com/r/test/comments/123/title"

        # Mock API response with empty selftext
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t3",
                            "data": {
                                "selftext": "",
                                "title": "Test Post"
                            }
                        }
                    ]
                }
            }
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_post_content(url)

        self.assertIn("has no text content", str(context.exception))

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_api_timeout(self, mock_get):
        """Test that ValueError is raised on API timeout."""
        # Given: Reddit URL
        url = "https://www.reddit.com/r/test/comments/123/title"

        # Mock timeout
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_post_content(url)

        self.assertIn("Request timeout", str(context.exception))

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_http_error(self, mock_get):
        """Test that ValueError is raised on HTTP error."""
        # Given: Reddit URL
        url = "https://www.reddit.com/r/test/comments/123/title"

        # Mock HTTP error
        import requests
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_get.return_value = mock_response

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_post_content(url)

        self.assertIn("Reddit API error", str(context.exception))

    @patch('trade_safety.reddit_extract_text_service.requests.get')
    def test_fetch_post_content_api_error(self, mock_get):
        """Test that ValueError is raised on general API error."""
        # Given: Reddit URL
        url = "https://www.reddit.com/r/test/comments/123/title"

        # Mock API error
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # When/Then: Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.service.fetch_post_content(url)

        self.assertIn("Failed to fetch Reddit post", str(context.exception))

    # ==============================================
    # Real HTTP Request Test
    # ==============================================

    def test_fetch_post_content_real_request(self):
        """Test fetching actual Reddit post content with real HTTP request."""
        # Given: Real Reddit URL
        url = (
            "https://www.reddit.com/r/mildlyinfuriating/comments/"
            "1pog0er/got_screwed_over_in_a_white_elephant_gift_exchange/"
        )

        try:
            # When: fetch_post_content is called with real HTTP request
            result = self.service.fetch_post_content(url)

            # Then: post content should be extracted
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

            # And: should contain expected content from the white elephant post
            self.assertIn("white elephant", result.lower())
            self.assertIn("green beans", result.lower())
            self.assertIn("Christmas party", result)

            print(f"\n✅ Successfully fetched Reddit post content: {len(result)} chars")
            print(f"✅ Post preview: {result[:200]}...")

        except ValueError as e:
            # If Reddit API is unavailable or rate limited
            print(f"\n⚠️ Reddit API call failed (this may be expected): {e}")
            self.skipTest(f"Reddit API unavailable: {e}")


if __name__ == "__main__":
    unittest.main()