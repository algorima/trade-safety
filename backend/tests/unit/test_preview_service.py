"""Unit tests for PreviewService."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock

from trade_safety.preview_service import PreviewService
from trade_safety.schemas import Platform
from trade_safety.twitter_extract_text_service import TweetMetadata, TwitterService


class TestPreviewService(unittest.TestCase):
    """Test PreviewService for post preview orchestration."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.twitter_service = MagicMock(spec=TwitterService)
        self.service = PreviewService(twitter_service=self.twitter_service)

    # ==============================================
    # preview() Tests - Twitter
    # ==============================================

    def test_preview_twitter_url_success(self):
        """Test successful preview for Twitter URL."""
        # Given: Twitter service returns metadata
        self.twitter_service.fetch_metadata.return_value = TweetMetadata(
            author="seller123",
            created_at=datetime(2024, 1, 20, 10, 30),
            text="급처분 포카 양도합니다. 자세한 내용은 DM으로 문의주세요. #급처 #양도 #photocard",
            images=["https://pbs.twimg.com/media/img1.jpg"],
        )

        # When: Preview Twitter URL
        result = self.service.preview("https://x.com/user/status/123")

        # Then: Correct preview returned
        self.assertEqual(result.platform, Platform.TWITTER)
        self.assertEqual(result.author, "seller123")
        self.assertEqual(
            result.text,
            "급처분 포카 양도합니다. 자세한 내용은 DM으로 문의주세요. #급처 #양도 #photocard",
        )
        self.assertEqual(
            result.text_preview,
            "급처분 포카 양도합니다. 자세한 내용은 DM으로 문의주세요. #급처 #양도 #photocard",
        )  # <200 chars
        self.assertEqual(len(result.images), 1)
        self.assertEqual(result.images[0], "https://pbs.twimg.com/media/img1.jpg")
        self.assertIsInstance(result.created_at, datetime)

    def test_preview_twitter_url_long_text(self):
        """Test preview with long text (truncation to 200 chars)."""
        # Given: Twitter service returns long text
        long_text = "포카 양도합니다. " * 50  # Very long text
        self.twitter_service.fetch_metadata.return_value = TweetMetadata(
            author="user1",
            created_at=datetime(2024, 1, 20, 10, 30),
            text=long_text,
            images=[],
        )

        # When: Preview
        result = self.service.preview("https://x.com/user/status/123")

        # Then: Text preview is truncated to 200 chars
        self.assertEqual(result.text, long_text)
        self.assertEqual(len(result.text_preview), 200)
        self.assertEqual(result.text_preview, long_text[:200])

    def test_preview_twitter_url_no_images(self):
        """Test preview for Twitter URL without images."""
        # Given: No images
        self.twitter_service.fetch_metadata.return_value = TweetMetadata(
            author="user1",
            created_at=datetime(2024, 1, 20, 10, 30),
            text="텍스트만 있는 트윗",
            images=[],
        )

        # When: Preview
        result = self.service.preview("https://x.com/user/status/123")

        # Then: Empty images list
        self.assertEqual(result.images, [])

    def test_preview_twitter_url_service_called(self):
        """Test that TwitterService.fetch_metadata is called correctly."""
        # Given
        self.twitter_service.fetch_metadata.return_value = TweetMetadata(
            author="user1",
            created_at=None,
            text="test",
            images=[],
        )

        # When
        self.service.preview("https://x.com/user/status/123456789")

        # Then: TwitterService called with correct URL
        self.twitter_service.fetch_metadata.assert_called_once_with(
            "https://x.com/user/status/123456789"
        )

    # ==============================================
    # preview() Tests - Reddit
    # ==============================================

    def test_preview_reddit_url_success(self):
        """Test successful preview for Reddit URL."""
        from datetime import datetime
        from unittest.mock import MagicMock

        from trade_safety.reddit_extract_text_service import (
            RedditPostMetadata,
            RedditService,
        )

        # Create Reddit service mock
        reddit_service = MagicMock(spec=RedditService)
        reddit_service.fetch_metadata.return_value = RedditPostMetadata(
            author="seller123",
            created_at=datetime(2024, 12, 26, 10, 30),
            title="[WTS][USA] Selling my entire kpop album collection",
            text="Cleaning out my collection. $5 each.",
            subreddit="kpopforsale",
            images=["https://i.redd.it/image.jpg"],
        )

        # Create service with Reddit mock
        service = PreviewService(
            twitter_service=self.twitter_service,
            reddit_service=reddit_service,
        )

        # When: Preview Reddit URL
        result = service.preview(
            "https://www.reddit.com/r/kpopforsale/comments/1ptmrbl/wtsusa_selling/"
        )

        # Then: Correct preview returned
        self.assertEqual(result.platform, Platform.REDDIT)
        self.assertEqual(result.author, "seller123")
        self.assertIn("[WTS][USA]", result.text)
        self.assertIn("Cleaning out", result.text)
        self.assertEqual(len(result.images), 1)

    def test_preview_reddit_service_called(self):
        """Test that RedditService.fetch_metadata is called correctly."""
        from datetime import datetime
        from unittest.mock import MagicMock

        from trade_safety.reddit_extract_text_service import (
            RedditPostMetadata,
            RedditService,
        )

        # Create Reddit service mock
        reddit_service = MagicMock(spec=RedditService)
        reddit_service.fetch_metadata.return_value = RedditPostMetadata(
            author="user1",
            created_at=None,
            title="Test",
            text="",
            subreddit="test",
            images=[],
        )

        service = PreviewService(
            twitter_service=self.twitter_service,
            reddit_service=reddit_service,
        )

        # When
        url = "https://www.reddit.com/r/kpopforsale/comments/abc123/title/"
        service.preview(url)

        # Then: RedditService called with correct URL
        reddit_service.fetch_metadata.assert_called_once_with(url)

    # ==============================================
    # Error Handling Tests
    # ==============================================

    def test_preview_unsupported_url(self):
        """Test error for unsupported URL (non-Twitter, non-Reddit)."""
        # Given: Non-supported URL
        unsupported_url = "https://facebook.com/post/123"

        # When/Then: ValueError raised
        with self.assertRaises(ValueError) as ctx:
            self.service.preview(unsupported_url)

        self.assertIn("Unsupported URL", str(ctx.exception))

    def test_preview_twitter_service_error(self):
        """Test error propagation from TwitterService."""
        # Given: TwitterService raises error
        self.twitter_service.fetch_metadata.side_effect = ValueError("Tweet not found")

        # When/Then: Error propagated
        with self.assertRaises(ValueError) as ctx:
            self.service.preview("https://x.com/user/status/123")

        self.assertIn("Tweet not found", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

