"""
Reddit Content Fetching Service.

This module provides functionality to fetch Reddit post content using OAuth 2.0.
Uses Client Credentials flow for server-to-server authentication.
"""

from __future__ import annotations

import base64
import logging
import re
from datetime import datetime, timedelta, timezone

import requests
from pydantic import BaseModel, Field

from trade_safety.settings import RedditAPISettings

logger = logging.getLogger(__name__)


# ==============================================================================
# Data Models
# ==============================================================================


class RedditPostMetadata(BaseModel):
    """Reddit post metadata for preview functionality"""

    author: str = Field(description="Post author username")
    created_at: datetime | None = Field(None, description="Post creation timestamp")
    title: str = Field(description="Post title")
    text: str = Field(description="Post text content (selftext)")
    subreddit: str = Field(description="Subreddit name")
    images: list[str] = Field(default_factory=list, description="Image URLs from post")


# ==============================================================================
# Reddit Service
# ==============================================================================


class RedditService:
    """
    Service for fetching Reddit post content using OAuth 2.0.

    This service uses Reddit's OAuth API with Client Credentials flow.
    Requires Reddit API Client ID and Secret (validated at API call time).

    Example:
        >>> from trade_safety.settings import RedditAPISettings
        >>> reddit_api = RedditAPISettings(client_id="ID", client_secret="SECRET")
        >>> service = RedditService(reddit_api)
        >>> metadata = service.fetch_metadata(
        ...     "https://www.reddit.com/r/kpopforsale/comments/abc123/wts_photocard/"
        ... )
        >>> print(metadata.title, metadata.author)

    Environment Variables:
        REDDIT_CLIENT_ID: Reddit App Client ID
        REDDIT_CLIENT_SECRET: Reddit App Client Secret
        REDDIT_USER_AGENT: Custom User-Agent (optional)
    """

    # OAuth token cache
    _access_token: str | None = None
    _token_expires_at: datetime | None = None

    def __init__(self, reddit_api: RedditAPISettings | None = None):
        """
        Initialize RedditService with Reddit API settings.

        Args:
            reddit_api: Reddit API settings containing client_id and client_secret.
                        If not provided, RedditAPISettings() will load from environment.

        Note:
            Credentials are validated at API call time (lazy validation),
            not at initialization.
        """
        self.settings = reddit_api or RedditAPISettings()
        logger.debug("Initialized RedditService")

    # ==========================================
    # Main Methods
    # ==========================================

    def fetch_metadata(self, reddit_url: str) -> RedditPostMetadata:
        """
        Fetch Reddit post metadata from URL using OAuth API.

        Args:
            reddit_url: Reddit post URL (e.g., https://reddit.com/r/sub/comments/id/title/)

        Returns:
            RedditPostMetadata: Post metadata including title, text, author, images

        Raises:
            ValueError: If credentials are missing, post ID extraction fails, or API fails

        Example:
            >>> service = RedditService()
            >>> metadata = service.fetch_metadata(
            ...     "https://www.reddit.com/r/kpopforsale/comments/abc123/wts_photocard/"
            ... )
        """
        # Extract post ID from URL
        post_id = self._extract_post_id(reddit_url)
        if not post_id:
            raise ValueError(f"Could not extract post ID from URL: {reddit_url}")

        # Get OAuth access token
        access_token = self._get_access_token()

        # Make API request
        data = self._make_api_request(post_id, access_token)

        # Parse response
        return self._parse_post_data(data)

    # ==========================================
    # OAuth Methods
    # ==========================================

    def _get_access_token(self) -> str:
        """
        Get OAuth access token using Client Credentials flow.

        Returns cached token if still valid, otherwise fetches new token.

        Returns:
            str: OAuth access token

        Raises:
            ValueError: If credentials are missing or token fetch fails
        """
        # Check if cached token is still valid
        if self._access_token and self._token_expires_at:
            if datetime.now(timezone.utc) < self._token_expires_at:
                logger.debug("Using cached OAuth token")
                return self._access_token

        # Validate credentials
        if not self.settings.client_id or not self.settings.client_secret:
            raise ValueError(
                "Reddit API credentials required. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables. "
                "Get credentials at: https://www.reddit.com/prefs/apps"
            )

        logger.info("Fetching new Reddit OAuth token")

        try:
            # Prepare auth header (Basic Auth with client_id:client_secret)
            credentials = f"{self.settings.client_id}:{self.settings.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "User-Agent": self.settings.user_agent,
            }
            data = {"grant_type": "client_credentials"}

            response = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                headers=headers,
                data=data,
                timeout=10,
            )
            response.raise_for_status()

            token_data = response.json()

            # Cache token
            self._access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            # Calculate expiration time with 60 second buffer
            self._token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)

            logger.info("Successfully obtained Reddit OAuth token")
            return self._access_token

        except requests.exceptions.HTTPError as e:
            error_msg = f"Reddit OAuth error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to obtain Reddit OAuth token: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    # ==========================================
    # API Request Methods
    # ==========================================

    def _make_api_request(self, post_id: str, access_token: str) -> dict:
        """
        Make Reddit OAuth API request to fetch post data.

        Args:
            post_id: Reddit post ID
            access_token: OAuth access token

        Returns:
            dict: API response JSON data

        Raises:
            ValueError: If API request fails
        """
        try:
            logger.debug("Making Reddit API request: post_id=%s", post_id)

            # Use OAuth API endpoint
            api_url = f"https://oauth.reddit.com/comments/{post_id}.json"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "User-Agent": self.settings.user_agent,
            }

            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout as exc:
            error_msg = f"Request timeout while fetching Reddit post: post_id={post_id}"
            logger.error(error_msg)
            raise ValueError(error_msg) from exc

        except requests.exceptions.HTTPError as e:
            error_msg = f"Reddit API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch Reddit post: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    def _parse_post_data(self, data: list) -> RedditPostMetadata:
        """
        Parse Reddit API response into RedditPostMetadata.

        Args:
            data: Reddit API response (list of listings)

        Returns:
            RedditPostMetadata: Parsed post metadata

        Raises:
            ValueError: If response structure is unexpected
        """
        try:
            # Reddit returns [post_listing, comments_listing]
            post_listing = data[0]
            post_data = post_listing["data"]["children"][0]["data"]

            # Extract author
            author = post_data.get("author", "unknown")

            # Extract created_at timestamp
            created_utc = post_data.get("created_utc")
            created_at = (
                datetime.fromtimestamp(created_utc, tz=timezone.utc)
                if created_utc
                else None
            )

            # Extract title and text
            title = post_data.get("title", "")
            selftext = post_data.get("selftext", "")

            # Extract subreddit
            subreddit = post_data.get("subreddit", "")

            # Extract images
            images = self._extract_images(post_data)

            metadata = RedditPostMetadata(
                author=author,
                created_at=created_at,
                title=title,
                text=selftext,
                subreddit=subreddit,
                images=images,
            )

            logger.info(
                "Successfully parsed Reddit post: author=%s, subreddit=%s, images=%d",
                metadata.author,
                metadata.subreddit,
                len(metadata.images),
            )

            return metadata

        except (KeyError, IndexError, TypeError) as e:
            error_msg = f"Failed to parse Reddit API response: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    def _extract_images(self, post_data: dict) -> list[str]:
        """
        Extract image URLs from Reddit post data.

        Args:
            post_data: Reddit post data dict

        Returns:
            list[str]: List of image URLs
        """
        images = []

        # Check for direct image URL
        url = post_data.get("url", "")
        if url and any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".gif"]):
            images.append(url)

        # Check for gallery images
        if post_data.get("is_gallery"):
            media_metadata = post_data.get("media_metadata", {})
            for media_id, media_info in media_metadata.items():
                if media_info.get("status") == "valid" and "s" in media_info:
                    # Get the source URL (highest quality)
                    source_url = media_info["s"].get("u", "")
                    if source_url:
                        # Reddit escapes HTML entities in URLs
                        source_url = source_url.replace("&amp;", "&")
                        images.append(source_url)

        # Check for preview images
        if not images and "preview" in post_data:
            preview_images = post_data["preview"].get("images", [])
            for img in preview_images:
                source = img.get("source", {})
                if source.get("url"):
                    url = source["url"].replace("&amp;", "&")
                    images.append(url)

        return images

    # ==========================================
    # Helper Methods
    # ==========================================

    def _extract_post_id(self, reddit_url: str) -> str | None:
        """
        Extract post ID from Reddit URL.

        Args:
            reddit_url: Reddit post URL

        Returns:
            Post ID if found, None otherwise

        Examples:
            >>> service = RedditService()
            >>> service._extract_post_id("https://reddit.com/r/sub/comments/abc123/title/")
            "abc123"
            >>> service._extract_post_id("https://redd.it/abc123")
            "abc123"
        """
        # Pattern for full Reddit URLs: /comments/{post_id}/
        pattern_full = r"/comments/([a-zA-Z0-9]+)"
        match = re.search(pattern_full, reddit_url)
        if match:
            post_id = match.group(1)
            logger.debug("Extracted Reddit post ID: %s", post_id)
            return post_id

        # Pattern for short URLs: redd.it/{post_id}
        pattern_short = r"redd\.it/([a-zA-Z0-9]+)"
        match = re.search(pattern_short, reddit_url)
        if match:
            post_id = match.group(1)
            logger.debug("Extracted Reddit post ID from short URL: %s", post_id)
            return post_id

        logger.warning("Could not extract post ID from URL: %s", reddit_url)
        return None

    # ==========================================
    # Utility Methods
    # ==========================================

    @staticmethod
    def is_reddit_url(url: str) -> bool:
        """
        Check if URL is a Reddit URL.

        Args:
            url: URL to check

        Returns:
            True if URL is from reddit.com or redd.it, False otherwise

        Examples:
            >>> RedditService.is_reddit_url("https://www.reddit.com/r/kpop/comments/abc/")
            True
            >>> RedditService.is_reddit_url("https://redd.it/abc123")
            True
            >>> RedditService.is_reddit_url("https://twitter.com/user/status/123")
            False
        """
        return "reddit.com" in url or "redd.it" in url
