"""
Preview Service for extracting social media post metadata.

This module orchestrates URL metadata extraction across supported platforms.
"""

from __future__ import annotations

import logging

from trade_safety.reddit_extract_text_service import RedditService
from trade_safety.schemas import Platform, PostPreview
from trade_safety.twitter_extract_text_service import TwitterService

logger = logging.getLogger(__name__)


class PreviewService:
    """
    Service for extracting post preview metadata from social media URLs.

    This service orchestrates platform-specific services (TwitterService, RedditService)
    to extract metadata for post previews.

    Supported platforms:
    - Twitter/X
    - Reddit

    Example:
        >>> service = PreviewService()
        >>> preview = service.preview("https://x.com/user/status/123")
        >>> print(preview.platform, preview.author)
        Platform.TWITTER seller123
    """

    def __init__(
        self,
        twitter_service: TwitterService | None = None,
        reddit_service: RedditService | None = None,
    ):
        """
        Initialize PreviewService with platform services.

        Args:
            twitter_service: TwitterService instance (default: None, auto-created)
            reddit_service: RedditService instance (default: None, auto-created)
        """
        self.twitter_service = twitter_service or TwitterService()
        self.reddit_service = reddit_service or RedditService()
        logger.debug("Initialized PreviewService")

    def preview(self, url: str) -> PostPreview:
        """
        Extract post preview metadata from URL.

        Args:
            url: Social media post URL (Twitter/X, Reddit)

        Returns:
            PostPreview: Post metadata including platform, author, text, images

        Raises:
            ValueError: If URL is not supported or extraction fails

        Example:
            >>> service = PreviewService()
            >>> preview = service.preview("https://x.com/user/status/123")
            >>> print(preview.platform)
            Platform.TWITTER
        """
        # Check if Twitter URL
        if TwitterService.is_twitter_url(url):
            logger.info("Detected Twitter URL, fetching metadata")
            twitter_metadata = self.twitter_service.fetch_metadata(url)

            # Truncate text to 200 characters for preview
            text_preview = (
                twitter_metadata.text[:200]
                if len(twitter_metadata.text) > 200
                else twitter_metadata.text
            )

            preview = PostPreview(
                platform=Platform.TWITTER,
                author=twitter_metadata.author,
                created_at=twitter_metadata.created_at,
                text=twitter_metadata.text,
                text_preview=text_preview,
                images=twitter_metadata.images,
            )

            logger.info(
                "Preview created: platform=%s, author=%s, images=%d",
                preview.platform,
                preview.author,
                len(preview.images),
            )

            return preview

        # Check if Reddit URL
        if RedditService.is_reddit_url(url):
            logger.info("Detected Reddit URL, fetching metadata")
            reddit_metadata = self.reddit_service.fetch_metadata(url)

            # Combine title and text for full content
            full_text = (
                f"{reddit_metadata.title}\n\n{reddit_metadata.text}"
                if reddit_metadata.text
                else reddit_metadata.title
            )

            # Truncate text to 200 characters for preview
            text_preview = full_text[:200] if len(full_text) > 200 else full_text

            preview = PostPreview(
                platform=Platform.REDDIT,
                author=reddit_metadata.author,
                created_at=reddit_metadata.created_at,
                text=full_text,
                text_preview=text_preview,
                images=reddit_metadata.images,
            )

            logger.info(
                "Preview created: platform=%s, author=%s, subreddit=%s, images=%d",
                preview.platform,
                preview.author,
                reddit_metadata.subreddit,
                len(preview.images),
            )

            return preview

        # Unsupported URL
        logger.warning("Unsupported URL: %s", url)
        raise ValueError(
            "Unsupported URL. Currently only Twitter/X and Reddit URLs are supported."
        )
