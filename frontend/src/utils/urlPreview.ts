import type { LinkPreviewData } from "@/components/UrlPreviewCard";

const SUPPORTED_DOMAINS = ["x.com", "twitter.com", "reddit.com"] as const;

/**
 * URL에서 도메인을 추출합니다.
 */
export function extractDomain(url: string): string | null {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace("www.", "");
  } catch {
    return null;
  }
}

/**
 * 텍스트에서 URL을 감지합니다.
 */
export function detectUrl(text: string): string | null {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const matches = text.match(urlRegex);

  if (!matches) {
    return null;
  }

  for (const url of matches) {
    const domain = extractDomain(url);
    if (domain && SUPPORTED_DOMAINS.some((d) => domain.includes(d))) {
      return url;
    }
  }

  return null;
}

/**
 * URL에서 메타데이터를 가져옵니다. (Mock 구현)
 */
export async function fetchUrlMetadata(
  url: string,
): Promise<LinkPreviewData | null> {
  const domain = extractDomain(url);

  if (!domain) {
    return null;
  }

  // Mock delay to simulate API call
  await new Promise((resolve) => setTimeout(resolve, 500));

  // Mock data based on domain
  if (domain.includes("x.com") || domain.includes("twitter.com")) {
    return MOCK_TWITTER_PREVIEW;
  }

  if (domain.includes("reddit.com")) {
    return MOCK_REDDIT_PREVIEW;
  }

  return null;
}

// Mock data for Storybook and testing
export const MOCK_TWITTER_PREVIEW: LinkPreviewData = {
  url: "https://x.com/crypto_expert/status/123456",
  title:
    "Breaking: Major cryptocurrency market update - Bitcoin reaches new milestone",
  author: "@crypto_expert",
  date: "2024-03-15",
  content:
    "🚨 BREAKING NEWS 🚨\n\nBitcoin just hit a new all-time high of $75,000! 📈\n\nThis is unprecedented growth in the crypto market. Many analysts predict this is just the beginning of a major bull run.\n\n💰 Investment opportunity of the decade?\n🔥 Get in now before it's too late!\n\nDM me for exclusive trading signals and investment advice. Limited spots available! 💎🙌\n\n#Bitcoin #Crypto #Investment #Trading #BTC",
  images: [
    "https://picsum.photos/seed/crypto1/800/600",
    "https://picsum.photos/seed/crypto2/800/600",
    "https://picsum.photos/seed/crypto3/800/600",
  ],
};

export const MOCK_REDDIT_PREVIEW: LinkPreviewData = {
  url: "https://reddit.com/r/security/comments/abc123",
  title: "Beware of this new cryptocurrency scam targeting beginners",
  author: "u/security_watchdog",
  date: "2024-03-14",
  content:
    '[WARNING] New Crypto Scam Alert!\n\nI\'ve been seeing a lot of posts lately about a "guaranteed 10x returns" investment scheme that\'s been making rounds on social media.\n\nHere are the red flags:\n- Promises unrealistic returns (500-1000% in weeks)\n- Asks you to send crypto to an unknown wallet\n- Claims to be affiliated with major exchanges (they\'re not)\n- Pressures you to "act now" or "limited spots"\n- Uses fake screenshots of profits\n\nPLEASE do your own research before investing. If it sounds too good to be true, it probably is.\n\nStay safe out there! 🛡️',
  images: [
    "https://picsum.photos/seed/reddit1/800/600",
    "https://picsum.photos/seed/reddit2/800/600",
  ],
};
