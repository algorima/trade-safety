"""Unit tests for RedditService."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import requests

from trade_safety.reddit_extract_text_service import RedditService
from trade_safety.settings import RedditAPISettings


class TestRedditService(unittest.TestCase):
    """Test RedditService for Reddit post content fetching."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Lazy validation: credentials not required at initialization
        self.service = RedditService()
        # Service with dummy credentials for API call tests
        self.service_with_creds = RedditService(
            reddit_api=RedditAPISettings(
                client_id="test-client-id",
                client_secret="test-client-secret",
            )
        )

    # ==============================================
    # URL Detection Tests
    # ==============================================

    def test_is_reddit_url_with_www(self):
        """Test that www.reddit.com URLs are detected as Reddit URLs."""
        url = "https://www.reddit.com/r/kpopforsale/comments/1ptmrbl/wtsusa_selling_my_entire_kpop_album_collection/"

        result = RedditService.is_reddit_url(url)

        self.assertTrue(result)

    def test_is_reddit_url_without_www(self):
        """Test that reddit.com URLs without www are detected."""
        url = "https://reddit.com/r/kpopforsale/comments/abc123/title/"

        result = RedditService.is_reddit_url(url)

        self.assertTrue(result)

    def test_is_reddit_url_with_short_url(self):
        """Test that redd.it short URLs are detected as Reddit URLs."""
        url = "https://redd.it/1ptmrbl"

        result = RedditService.is_reddit_url(url)

        self.assertTrue(result)

    def test_is_reddit_url_with_non_reddit_domain(self):
        """Test that non-Reddit URLs are not detected as Reddit URLs."""
        url = "https://twitter.com/user/status/123"

        result = RedditService.is_reddit_url(url)

        self.assertFalse(result)

    # ==============================================
    # Post ID Extraction Tests
    # ==============================================

    def test_extract_post_id_from_full_url(self):
        """Test extracting post ID from full Reddit URL."""
        url = "https://www.reddit.com/r/kpopforsale/comments/1ptmrbl/wtsusa_selling_my_entire_kpop_album_collection/"

        post_id = self.service._extract_post_id(url)

        self.assertEqual(post_id, "1ptmrbl")

    def test_extract_post_id_from_short_url(self):
        """Test extracting post ID from redd.it short URL."""
        url = "https://redd.it/1ptmrbl"

        post_id = self.service._extract_post_id(url)

        self.assertEqual(post_id, "1ptmrbl")

    def test_extract_post_id_with_query_params(self):
        """Test extracting post ID from URL with query parameters."""
        url = "https://www.reddit.com/r/kpopforsale/comments/abc123/title/?utm_source=share"

        post_id = self.service._extract_post_id(url)

        self.assertEqual(post_id, "abc123")

    def test_extract_post_id_from_invalid_url(self):
        """Test that None is returned for invalid Reddit URL."""
        url = "https://www.reddit.com/r/kpopforsale/"

        post_id = self.service._extract_post_id(url)

        self.assertIsNone(post_id)

    # ==============================================
    # OAuth Token Tests
    # ==============================================

    def test_get_access_token_missing_credentials(self):
        """Test that ValueError is raised when credentials are missing."""
        # Service without credentials
        service = RedditService(
            reddit_api=RedditAPISettings(client_id=None, client_secret=None)
        )

        with self.assertRaises(ValueError) as context:
            service._get_access_token()

        self.assertIn("Reddit API credentials required", str(context.exception))

    @patch("trade_safety.reddit_extract_text_service.requests.post")
    def test_get_access_token_success(self, mock_post):
        """Test successful OAuth token fetch."""
        # Mock OAuth response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3600,
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        token = self.service_with_creds._get_access_token()

        self.assertEqual(token, "test-access-token")
        mock_post.assert_called_once()

    @patch("trade_safety.reddit_extract_text_service.requests.post")
    def test_get_access_token_caching(self, mock_post):
        """Test that token is cached and reused."""
        # Mock OAuth response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3600,
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # First call - fetch token
        token1 = self.service_with_creds._get_access_token()
        # Second call - should use cached token
        token2 = self.service_with_creds._get_access_token()

        self.assertEqual(token1, token2)
        # Should only call API once due to caching
        self.assertEqual(mock_post.call_count, 1)

    # ==============================================
    # Fetch Metadata Tests
    # ==============================================

    @patch("trade_safety.reddit_extract_text_service.requests.get")
    @patch("trade_safety.reddit_extract_text_service.requests.post")
    def test_fetch_metadata_success(self, mock_post, mock_get):
        """Test fetching Reddit post metadata with mocked API response."""
        # Mock OAuth response
        mock_oauth_response = MagicMock()
        mock_oauth_response.json.return_value = {
            "access_token": "test-token",
            "expires_in": 3600,
        }
        mock_oauth_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_oauth_response

        # Mock Reddit API response
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = [
            {
                "data": {
                    "children": [
                        {
                            "data": {
                                "author": "seller123",
                                "title": "[WTS][USA] Selling my entire kpop album collection",
                                "selftext": "Cleaning out my collection. $5 each.",
                                "subreddit": "kpopforsale",
                                "created_utc": 1735200000,
                                "url": "https://i.redd.it/image.jpg",
                            }
                        }
                    ]
                }
            },
            {"data": {"children": []}},  # Comments listing
        ]
        mock_api_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_api_response

        # Call fetch_metadata
        url = "https://www.reddit.com/r/kpopforsale/comments/1ptmrbl/wtsusa_selling_my_entire_kpop_album_collection/"
        metadata = self.service_with_creds.fetch_metadata(url)

        # Verify result
        self.assertEqual(metadata.author, "seller123")
        self.assertEqual(
            metadata.title, "[WTS][USA] Selling my entire kpop album collection"
        )
        self.assertEqual(metadata.text, "Cleaning out my collection. $5 each.")
        self.assertEqual(metadata.subreddit, "kpopforsale")
        self.assertIsInstance(metadata.created_at, datetime)
        self.assertIn("https://i.redd.it/image.jpg", metadata.images)

    @patch("trade_safety.reddit_extract_text_service.requests.get")
    @patch("trade_safety.reddit_extract_text_service.requests.post")
    def test_fetch_metadata_invalid_url(self, _mock_post, _mock_get):
        """Test that ValueError is raised for invalid Reddit URL."""
        url = "https://www.reddit.com/r/kpopforsale/"

        with self.assertRaises(ValueError) as context:
            self.service_with_creds.fetch_metadata(url)

        self.assertIn("Could not extract post ID", str(context.exception))

    @patch("trade_safety.reddit_extract_text_service.requests.get")
    @patch("trade_safety.reddit_extract_text_service.requests.post")
    def test_fetch_metadata_api_timeout(self, mock_post, mock_get):
        """Test that ValueError is raised on API timeout."""
        # Mock OAuth success
        mock_oauth_response = MagicMock()
        mock_oauth_response.json.return_value = {
            "access_token": "test",
            "expires_in": 3600,
        }
        mock_oauth_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_oauth_response

        # Mock API timeout
        mock_get.side_effect = requests.exceptions.Timeout()

        url = "https://www.reddit.com/r/kpopforsale/comments/abc123/title/"

        with self.assertRaises(ValueError) as context:
            self.service_with_creds.fetch_metadata(url)

        self.assertIn("Request timeout", str(context.exception))

    # ==============================================
    # Image Extraction Tests
    # ==============================================

    def test_extract_images_direct_url(self):
        """Test extracting image from direct URL."""
        post_data = {
            "url": "https://i.redd.it/example.jpg",
            "is_gallery": False,
        }

        images = self.service._extract_images(post_data)

        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], "https://i.redd.it/example.jpg")

    def test_extract_images_gallery(self):
        """Test extracting images from gallery post."""
        post_data = {
            "url": "https://www.reddit.com/gallery/abc123",
            "is_gallery": True,
            "media_metadata": {
                "img1": {"status": "valid", "s": {"u": "https://i.redd.it/img1.jpg"}},
                "img2": {"status": "valid", "s": {"u": "https://i.redd.it/img2.jpg"}},
            },
        }

        images = self.service._extract_images(post_data)

        self.assertEqual(len(images), 2)

    def test_extract_images_no_images(self):
        """Test that empty list is returned when no images."""
        post_data = {
            "url": "https://www.reddit.com/r/kpopforsale/comments/abc/",
            "is_gallery": False,
        }

        images = self.service._extract_images(post_data)

        self.assertEqual(images, [])


if __name__ == "__main__":
    unittest.main()
