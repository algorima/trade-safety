"""
Twitter Content Fetching Service.

This module provides functionality to fetch tweet content from Twitter/X URLs
using the official Twitter API v2.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime

import requests
from pydantic import BaseModel, Field

from trade_safety.settings import TwitterAPISettings

logger = logging.getLogger(__name__)


# ==============================================================================
# Data Models
# ==============================================================================


class TweetMetadata(BaseModel):
    """Tweet metadata for preview functionality"""

    author: str = Field(description="Tweet author username")
    created_at: datetime | None = Field(None, description="Tweet creation timestamp")
    text: str = Field(description="Tweet text content")
    images: list[str] = Field(default_factory=list, description="Image URLs from tweet")


# ==============================================================================
# Twitter Service
# ==============================================================================


class TwitterService:
    """
    Service for fetching tweet content from Twitter/X URLs.

    This service uses the official Twitter API v2 to fetch tweet content.
    Requires a Twitter API Bearer Token (validated at API call time, not initialization).

    Example:
        >>> from trade_safety.settings import TwitterAPISettings
        >>> twitter_api = TwitterAPISettings(bearer_token="YOUR_BEARER_TOKEN")
        >>> service = TwitterService(twitter_api)
        >>> tweet_text = service.fetch_tweet_content(
        ...     "https://x.com/user/status/123456789"
        ... )
        >>> print(tweet_text)
        "급처분 포카 양도합니다..."

    Environment Variables:
        TWITTER_BEARER_TOKEN: Twitter API Bearer Token (auto-loaded via TwitterAPISettings)
    """

    def __init__(self, twitter_api: TwitterAPISettings | None = None):
        """
        Initialize TwitterService with Twitter API settings.

        Args:
            twitter_api: Twitter API settings containing bearer_token.
                         If not provided, TwitterAPISettings() will load from environment.

        Note:
            Bearer token is validated at API call time (lazy validation),
            not at initialization. This allows unit tests to create the service
            without providing a token when using mocks.
        """
        self.settings = twitter_api or TwitterAPISettings()
        logger.debug("Initialized TwitterService")

    # ==========================================
    # Main Methods
    # ==========================================

    def fetch_tweet_content(self, twitter_url: str) -> str:
        """
        Fetch tweet content from Twitter/X URL using Twitter API v2.

        Args:
            twitter_url: Twitter/X URL (e.g., https://x.com/user/status/123456789)

        Returns:
            str: Tweet text content

        Raises:
            ValueError: If bearer token is missing, tweet ID extraction fails, or API call fails

        Example:
            >>> from trade_safety.settings import TwitterAPISettings
            >>> service = TwitterService(TwitterAPISettings(bearer_token="YOUR_TOKEN"))
            >>> content = service.fetch_tweet_content(
            ...     "https://x.com/mkticket7/status/2000111727493718384"
            ... )
        """
        # Extract tweet ID from URL
        tweet_id = self._extract_tweet_id(twitter_url)
        if not tweet_id:
            raise ValueError(f"Could not extract tweet ID from URL: {twitter_url}")

        # Make API request
        params = {"tweet.fields": "text"}
        data = self._make_api_request(tweet_id, params)

        # Validate and extract text
        if "data" not in data or "text" not in data["data"]:
            raise ValueError(f"Tweet not found or inaccessible: {tweet_id}")

        tweet_text = data["data"]["text"]
        logger.info("Successfully fetched tweet: %d chars", len(tweet_text))

        return tweet_text

    def fetch_metadata(self, twitter_url: str) -> TweetMetadata:
        """
        Fetch tweet metadata from Twitter/X URL for post preview.

        This method retrieves comprehensive metadata including author, timestamp,
        text content, and image URLs. Used for post preview functionality.

        Args:
            twitter_url: Twitter/X URL (e.g., https://x.com/user/status/123456789)

        Returns:
            TweetMetadata: Tweet metadata including author, created_at, text, and images

        Raises:
            ValueError: If bearer token is missing, tweet ID extraction fails, or API call fails

        Example:
            >>> service = TwitterService(TwitterAPISettings(bearer_token="YOUR_TOKEN"))
            >>> metadata = service.fetch_metadata("https://x.com/user/status/123")
            >>> print(metadata.author, len(metadata.images))
            seller123 2
        """
        # Extract tweet ID from URL
        tweet_id = self._extract_tweet_id(twitter_url)
        if not tweet_id:
            raise ValueError(f"Could not extract tweet ID from URL: {twitter_url}")

        # Make API request with extended fields
        params = {
            "tweet.fields": "text,created_at,attachments",
            "expansions": "author_id,attachments.media_keys",
            "user.fields": "username",
            "media.fields": "type,url",
        }
        data = self._make_api_request(tweet_id, params)

        # Validate response structure
        if "data" not in data or "text" not in data["data"]:
            raise ValueError(f"Tweet not found or inaccessible: {tweet_id}")

        tweet_data = data["data"]
        includes = data.get("includes", {})

        # Extract author username
        users = includes.get("users", [])
        author = users[0]["username"] if users else "unknown"

        # Extract created_at timestamp
        created_at_str = tweet_data.get("created_at")
        created_at = (
            datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            if created_at_str
            else None
        )

        # Extract text
        text = tweet_data["text"]

        # Extract image URLs (photos only, filter out videos)
        images = []
        media_list = includes.get("media", [])
        for media in media_list:
            if media.get("type") == "photo" and "url" in media:
                images.append(media["url"])

        metadata = TweetMetadata(
            author=author,
            created_at=created_at,
            text=text,
            images=images,
        )

        logger.info(
            "Successfully fetched tweet metadata: author=%s, images=%d",
            metadata.author,
            len(metadata.images),
        )

        return metadata

    # ==========================================
    # Helper Methods
    # ==========================================

    def _extract_tweet_id(self, twitter_url: str) -> str | None:
        """
        Extract tweet ID from Twitter/X URL.

        Args:
            twitter_url: Twitter/X URL

        Returns:
            Tweet ID if found, None otherwise

        Examples:
            >>> service = TwitterService()
            >>> service._extract_tweet_id("https://x.com/user/status/123456789")
            "123456789"
            >>> service._extract_tweet_id("https://twitter.com/user/status/987654321?s=20")
            "987654321"
        """
        # 패턴 분석
        pattern = r"/status/(\d+)"
        match = re.search(pattern, twitter_url)

        if match:
            tweet_id = match.group(1)
            logger.debug("Extracted tweet ID: %s", tweet_id)
            return tweet_id

        logger.warning("Could not extract tweet ID from URL: %s", twitter_url)
        return None

    def _make_api_request(self, tweet_id: str, params: dict) -> dict:
        """
        Make Twitter API v2 request with common headers and error handling.

        Args:
            tweet_id: Tweet ID to fetch
            params: Query parameters for the API request

        Returns:
            dict: API response JSON data

        Raises:
            ValueError: If API request fails
        """
        # Validate bearer token
        # Lazy validation: check bearer token at call time
        if not self.settings.bearer_token:
            raise ValueError(
                "Twitter Bearer Token is required. "
                "Provide it via TwitterAPISettings or TWITTER_BEARER_TOKEN environment variable. "
                "Get your token at: https://developer.twitter.com/en/portal/dashboard"
            )

        try:
            logger.debug("Making Twitter API v2 request: tweet_id=%s", tweet_id)

            api_url = f"https://api.twitter.com/2/tweets/{tweet_id}"
            headers = {
                "Authorization": f"Bearer {self.settings.bearer_token}",
                "User-Agent": "v2TweetLookupPython",
            }

            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout as exc:
            error_msg = f"Request timeout while fetching tweet: tweet_id={tweet_id}"
            logger.error(error_msg)
            raise ValueError(error_msg) from exc

        except requests.exceptions.HTTPError as e:
            error_msg = (
                f"Twitter API error: {e.response.status_code} - {e.response.text}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg) from e

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch tweet from API: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    # ==========================================
    # Utility Methods
    # ==========================================

    @staticmethod
    def is_twitter_url(url: str) -> bool:
        """
        Check if URL is a Twitter/X URL.

        Args:
            url: URL to check

        Returns:
            True if URL is from twitter.com or x.com, False otherwise

        Examples:
            >>> TwitterService.is_twitter_url("https://x.com/user/status/123")
            True
            >>> TwitterService.is_twitter_url("https://twitter.com/user/status/123")
            True
            >>> TwitterService.is_twitter_url("https://example.com")
            False
        """
        return "twitter.com" in url or "x.com" in url
