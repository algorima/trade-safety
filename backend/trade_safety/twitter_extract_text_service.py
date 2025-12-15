"""
Twitter Content Fetching Service.

This module provides functionality to fetch tweet content from Twitter/X URLs
using the official Twitter API v2.
"""

from __future__ import annotations

import logging
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# ==============================================================================
# Twitter Service
# ==============================================================================


class TwitterService:
    """
    Service for fetching tweet content from Twitter/X URLs.

    This service uses the official Twitter API v2 to fetch tweet content.
    Requires a Twitter API Bearer Token.

    Example:
        >>> service = TwitterService(bearer_token="YOUR_BEARER_TOKEN")
        >>> tweet_text = service.fetch_tweet_content(
        ...     "https://x.com/user/status/123456789"
        ... )
        >>> print(tweet_text)
        "급처분 포카 양도합니다..."

    Environment Variables:
        TWITTER_BEARER_TOKEN: Twitter API Bearer Token (optional if passed to __init__)
    """

    def __init__(self, bearer_token: str | None = None):
        """
        Initialize TwitterService with Twitter API credentials.

        Args:
            bearer_token: Twitter API Bearer Token.
                         If not provided, will try to read from TWITTER_BEARER_TOKEN env var.

        Raises:
            ValueError: If bearer_token is not provided and TWITTER_BEARER_TOKEN env var is not set
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')

        if not self.bearer_token:
            raise ValueError(
                "Twitter Bearer Token is required. "
                "Provide it via bearer_token parameter or TWITTER_BEARER_TOKEN environment variable. "
                "Get your token at: https://developer.twitter.com/en/portal/dashboard"
            )

        logger.debug("Initialized TwitterService with Bearer Token")

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
            ValueError: If tweet ID extraction or API call fails

        Example:
            >>> service = TwitterService(bearer_token="YOUR_TOKEN")
            >>> content = service.fetch_tweet_content(
            ...     "https://x.com/mkticket7/status/2000111727493718384"
            ... )
        """
        # URL에서 트위터 ID 추출
        tweet_id = self._extract_tweet_id(twitter_url)
        if not tweet_id:
            raise ValueError(f"Could not extract tweet ID from URL: {twitter_url}")


        try:
            logger.debug("Fetching tweet from Twitter API v2: tweet_id=%s", tweet_id)

            # 트위터 API 사용
            api_url = f"https://api.twitter.com/2/tweets/{tweet_id}"

            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'v2TweetLookupPython'
            }

            params = {
                'tweet.fields': 'text'
            }

            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # response에서 트윗 ID 추출
            if 'data' not in data or 'text' not in data['data']:
                raise ValueError(f"Tweet not found or inaccessible: {tweet_id}")

            tweet_text = data['data']['text']
            logger.info("Successfully fetched tweet: %d chars", len(tweet_text))

            return tweet_text

        except requests.exceptions.Timeout:
            error_msg = f"Request timeout while fetching tweet: {twitter_url}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        except requests.exceptions.HTTPError as e:
            error_msg = f"Twitter API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch tweet from API: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

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
            >>> service = TwitterService(bearer_token="token")
            >>> service._extract_tweet_id("https://x.com/user/status/123456789")
            "123456789"
            >>> service._extract_tweet_id("https://twitter.com/user/status/987654321?s=20")
            "987654321"
        """
        # 패턴 분석
        pattern = r'/status/(\d+)'
        match = re.search(pattern, twitter_url)

        if match:
            tweet_id = match.group(1)
            logger.debug("Extracted tweet ID: %s", tweet_id)
            return tweet_id

        logger.warning("Could not extract tweet ID from URL: %s", twitter_url)
        return None

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
        return 'twitter.com' in url or 'x.com' in url