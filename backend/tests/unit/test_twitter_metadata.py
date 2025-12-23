"""Unit tests for TwitterService.fetch_metadata()."""

import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import requests

from trade_safety.settings import TwitterAPISettings
from trade_safety.twitter_extract_text_service import TweetMetadata, TwitterService


class TestTwitterMetadata(unittest.TestCase):
    """Test TwitterService metadata fetching for post previews."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = TwitterService(
            twitter_api=TwitterAPISettings(bearer_token="test-token")
        )

    # ==============================================
    # fetch_metadata() Tests
    # ==============================================

    @patch("requests.get")
    def test_fetch_metadata_success_with_images(self, mock_get):
        """Test successful metadata fetch with images."""
        # Given: Twitter API response with images
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": "123456789",
                "text": "급처분 포카 양도합니다",
                "created_at": "2024-01-20T10:30:00.000Z",
                "attachments": {"media_keys": ["media1"]},
            },
            "includes": {
                "users": [{"id": "user1", "username": "seller123"}],
                "media": [
                    {
                        "media_key": "media1",
                        "type": "photo",
                        "url": "https://pbs.twimg.com/media/image1.jpg",
                    }
                ],
            },
        }
        mock_get.return_value = mock_response

        # When: Fetch metadata
        result = self.service.fetch_metadata("https://x.com/user/status/123456789")

        # Then: Correct metadata returned
        self.assertEqual(result.author, "seller123")
        self.assertEqual(result.text, "급처분 포카 양도합니다")
        self.assertEqual(len(result.images), 1)
        self.assertEqual(result.images[0], "https://pbs.twimg.com/media/image1.jpg")
        self.assertIsInstance(result.created_at, datetime)

    @patch("requests.get")
    def test_fetch_metadata_success_without_images(self, mock_get):
        """Test successful metadata fetch without images."""
        # Given: Twitter API response without images
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "text": "텍스트만 있는 트윗",
                "created_at": "2024-01-20T10:30:00.000Z",
            },
            "includes": {"users": [{"id": "u1", "username": "user1"}]},
        }
        mock_get.return_value = mock_response

        # When
        result = self.service.fetch_metadata("https://x.com/user/status/123")

        # Then: Empty images list
        self.assertEqual(result.author, "user1")
        self.assertEqual(result.text, "텍스트만 있는 트윗")
        self.assertEqual(result.images, [])

    @patch("requests.get")
    def test_fetch_metadata_multiple_images(self, mock_get):
        """Test metadata fetch with multiple images."""
        # Given: Twitter API response with multiple images
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "text": "여러 이미지",
                "created_at": "2024-01-20T10:30:00.000Z",
                "attachments": {"media_keys": ["m1", "m2", "m3"]},
            },
            "includes": {
                "users": [{"username": "user1"}],
                "media": [
                    {"media_key": "m1", "type": "photo", "url": "https://img1.jpg"},
                    {"media_key": "m2", "type": "photo", "url": "https://img2.jpg"},
                    {"media_key": "m3", "type": "photo", "url": "https://img3.jpg"},
                ],
            },
        }
        mock_get.return_value = mock_response

        # When
        result = self.service.fetch_metadata("https://x.com/user/status/123")

        # Then: All images returned
        self.assertEqual(len(result.images), 3)
        self.assertIn("https://img1.jpg", result.images)
        self.assertIn("https://img2.jpg", result.images)

    @patch("requests.get")
    def test_fetch_metadata_filter_video_media(self, mock_get):
        """Test that video media is filtered out (photos only)."""
        # Given: Mix of photo and video
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "text": "포토와 비디오",
                "created_at": "2024-01-20T10:30:00.000Z",
                "attachments": {"media_keys": ["m1", "m2"]},
            },
            "includes": {
                "users": [{"username": "user1"}],
                "media": [
                    {"media_key": "m1", "type": "photo", "url": "https://img.jpg"},
                    {"media_key": "m2", "type": "video", "url": "https://video.mp4"},
                ],
            },
        }
        mock_get.return_value = mock_response

        # When
        result = self.service.fetch_metadata("https://x.com/user/status/123")

        # Then: Only photo returned
        self.assertEqual(len(result.images), 1)
        self.assertEqual(result.images[0], "https://img.jpg")

    @patch("requests.get")
    def test_fetch_metadata_api_error(self, mock_get):
        """Test API error handling."""
        # Given: API returns error with response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_get.side_effect = http_error

        # When/Then: ValueError raised
        with self.assertRaises(ValueError):
            self.service.fetch_metadata("https://x.com/user/status/123")

    @patch("requests.get")
    def test_fetch_metadata_invalid_url(self, mock_get):
        """Test invalid URL handling."""
        # When/Then: ValueError raised for invalid URL
        with self.assertRaises(ValueError) as ctx:
            self.service.fetch_metadata("https://x.com/invalid-url")

        self.assertIn("Could not extract tweet ID", str(ctx.exception))

    def test_fetch_metadata_missing_bearer_token(self):
        """Test error when bearer token is missing."""
        # Given: Service without token
        service_no_token = TwitterService(twitter_api=TwitterAPISettings())

        # When/Then: ValueError raised
        with self.assertRaises(ValueError) as ctx:
            service_no_token.fetch_metadata("https://x.com/user/status/123")

        self.assertIn("Twitter Bearer Token is required", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
