"""
Reddit Content Fetching Service.

This module provides functionality to fetch post content from Reddit URLs
using Reddit's JSON API.
"""

from __future__ import annotations

import logging
import re

import requests

logger = logging.getLogger(__name__)


# ==============================================================================
# Reddit Service
# ==============================================================================


class RedditService:
    """
    Service for fetching Reddit post content from Reddit URLs.

    This service uses Reddit's JSON API to fetch post content.
    No authentication required for public posts.

    Example:
        >>> service = RedditService()
        >>> post_text = service.fetch_post_content(
        ...     "https://www.reddit.com/r/mildlyinfuriating/comments/1pog0er/got_screwed_over"
        ... )
        >>> print(post_text)
        "So last night I was at at Christmas party..."

    Note:
        Reddit's JSON API is accessed by appending .json to any Reddit URL.
    """

    def __init__(self):
        """Initialize RedditService."""
        logger.debug("Initialized RedditService")

    # ==========================================
    # Main Methods
    # ==========================================

    def fetch_post_content(self, reddit_url: str) -> str:
        """
        Fetch Reddit post content from Reddit URL using JSON API.

        Args:
            reddit_url: Reddit post URL (e.g., https://www.reddit.com/r/subreddit/comments/...)

        Returns:
            str: Post selftext content

        Raises:
            ValueError: If post extraction or API call fails

        Example:
            >>> service = RedditService()
            >>> content = service.fetch_post_content(
            ...     "https://www.reddit.com/r/mildlyinfuriating/comments/1pog0er/title"
            ... )
        """
        # Validate Reddit URL
        if not self.is_reddit_url(reddit_url):
            raise ValueError(f"Invalid Reddit URL: {reddit_url}")

        # Clean URL and add .json extension
        json_url = self._convert_to_json_url(reddit_url)

        try:
            logger.debug("Fetching Reddit post from JSON API: url=%s", json_url)

            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; RedditContentFetcher/1.0)"
            }

            response = requests.get(json_url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract selftext from Reddit JSON response
            selftext = self._extract_selftext(data)

            if not selftext:
                raise ValueError(f"Post not found or has no text content: {reddit_url}")

            logger.info("Successfully fetched Reddit post: %d chars", len(selftext))

            return selftext

        except requests.exceptions.Timeout as exc:
            error_msg = f"Request timeout while fetching Reddit post: {reddit_url}"
            logger.error(error_msg)
            raise ValueError(error_msg) from exc

        except requests.exceptions.HTTPError as e:
            error_msg = (
                f"Reddit API error: {e.response.status_code} - {e.response.text}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg) from e

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch Reddit post from API: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    # ==========================================
    # Helper Methods
    # ==========================================

    def _convert_to_json_url(self, reddit_url: str) -> str:
        """
        Convert Reddit URL to JSON API URL by appending .json.

        Args:
            reddit_url: Reddit post URL

        Returns:
            JSON API URL

        Examples:
            >>> service = RedditService()
            >>> service._convert_to_json_url("https://www.reddit.com/r/test/comments/123/title")
            "https://www.reddit.com/r/test/comments/123/title.json"
            >>> service._convert_to_json_url("https://www.reddit.com/r/test/comments/123/title.json")
            "https://www.reddit.com/r/test/comments/123/title.json"
        """
        # Remove trailing slash if exists
        clean_url = reddit_url.rstrip("/")

        # Check if .json already exists
        if clean_url.endswith(".json"):
            return clean_url

        # Add .json extension
        json_url = f"{clean_url}.json"
        logger.debug("Converted to JSON URL: %s", json_url)

        return json_url

    def _extract_selftext(self, json_data: dict) -> str | None:
        """
        Extract selftext from Reddit JSON response.

        Reddit JSON structure:
        [
          {
            "kind": "Listing",
            "data": {
              "children": [
                {
                  "kind": "t3",
                  "data": {
                    "selftext": "Post content here..."
                  }
                }
              ]
            }
          }
        ]

        Args:
            json_data: Reddit JSON response

        Returns:
            Selftext content if found, None otherwise

        Example:
            >>> service = RedditService()
            >>> data = [{"data": {"children": [{"data": {"selftext": "Hello"}}]}}]
            >>> service._extract_selftext(data)
            "Hello"
        """
        try:
            # Reddit JSON response is a list
            if isinstance(json_data, list) and len(json_data) > 0:
                # First element contains the post data
                post_listing = json_data[0]

                # Navigate through the JSON structure
                if "data" in post_listing:
                    children = post_listing["data"].get("children", [])

                    if children and len(children) > 0:
                        post_data = children[0].get("data", {})
                        selftext = post_data.get("selftext", "")

                        if selftext:
                            logger.debug("Extracted selftext: %d chars", len(selftext))
                            return selftext

            logger.warning("Could not find selftext in Reddit JSON response")
            return None

        except (KeyError, IndexError, TypeError) as e:
            logger.error("Error extracting selftext from Reddit JSON: %s", str(e))
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
            True if URL is from reddit.com, False otherwise

        Examples:
            >>> RedditService.is_reddit_url("https://www.reddit.com/r/test/comments/123")
            True
            >>> RedditService.is_reddit_url("https://reddit.com/r/test/comments/123")
            True
            >>> RedditService.is_reddit_url("https://example.com")
            False
        """
        return "reddit.com" in url

    @staticmethod
    def extract_post_id(reddit_url: str) -> str | None:
        """
        Extract post ID from Reddit URL.

        Args:
            reddit_url: Reddit URL

        Returns:
            Post ID if found, None otherwise

        Examples:
            >>> RedditService.extract_post_id(
            ...     "https://www.reddit.com/r/test/comments/1pog0er/title"
            ... )
            "1pog0er"
        """
        # Pattern: /comments/{post_id}/
        pattern = r"/comments/([a-z0-9]+)"
        match = re.search(pattern, reddit_url)

        if match:
            post_id = match.group(1)
            logger.debug("Extracted post ID: %s", post_id)
            return post_id

        logger.warning("Could not extract post ID from URL: %s", reddit_url)
        return None
