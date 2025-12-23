"""
Preview Service for extracting social media post metadata.

This module orchestrates URL metadata extraction across supported platforms.
"""

from __future__ import annotations

import logging

from trade_safety.schemas import Platform, PostPreview
from trade_safety.twitter_extract_text_service import TwitterService

logger = logging.getLogger(__name__)


class PreviewService:
    """
    Service for extracting post preview metadata from social media URLs.

    This service orchestrates platform-specific services (TwitterService)
    to extract metadata for post previews.

    Supported platforms:
    - Twitter/X

    Example:
        >>> service = PreviewService()
        >>> preview = service.preview("https://x.com/user/status/123")
        >>> print(preview.platform, preview.author)
        Platform.TWITTER seller123
    """

    def __init__(
        self, twitter_service: TwitterService | None = None
    ):
        """
        Initialize PreviewService with platform services.

        Args:
            twitter_service: TwitterService instance (default: None, auto-created)
        """
        self.twitter_service = twitter_service or TwitterService()
        logger.debug("Initialized PreviewService")

    def preview(self, url: str) -> PostPreview:
        """
        Extract post preview metadata from URL.

        Args:
            url: Social media post URL (Twitter/X)

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
        # Implementation to be added
        raise NotImplementedError("preview() not yet implemented")
