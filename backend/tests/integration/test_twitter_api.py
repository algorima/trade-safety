"""Integration tests for Twitter API."""

import unittest

from trade_safety.settings import TwitterAPISettings
from trade_safety.twitter_extract_text_service import TwitterService


class TestTwitterAPIIntegration(unittest.TestCase):
    """Integration tests for TwitterService with real API calls."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Load bearer token from environment via Settings
        twitter_api = TwitterAPISettings()
        if not twitter_api.bearer_token:
            self.skipTest("TWITTER_BEARER_TOKEN not configured")
        self.service = TwitterService(twitter_api=twitter_api)

    def test_fetch_tweet_content_real_request(self):
        """Test fetching actual tweet content from Twitter API with real HTTP request."""
        # Given: Real Twitter URL
        url = "https://x.com/mkticket7/status/2000111727493718384?s=20"

        try:
            # When: fetch_tweet_content is called with real HTTP request
            result = self.service.fetch_tweet_content(url)

            # Then: tweet text should be extracted
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

            # And: should contain expected content
            self.assertIn("권진아", result)  # Artist name
            self.assertIn("티켓", result)  # Ticket keyword

            print(f"\n✅ Successfully fetched tweet content: {len(result)} chars")
            print(f"✅ Tweet preview: {result}...")

        except ValueError as e:
            # If Twitter API requires authentication or rate limits
            print(f"\n⚠️ Twitter API call failed (this may be expected): {e}")
            self.skipTest(f"Twitter API unavailable: {e}")


if __name__ == "__main__":
    unittest.main()
