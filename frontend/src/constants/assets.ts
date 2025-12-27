import { SafetyLevel } from "@/types";

export interface EmojiAssets {
  lottie: string;
  webp: string;
  gif: string;
  alt: string;
}

export const EMOJI_ASSETS: Record<SafetyLevel, EmojiAssets> = {
  danger: {
    lottie: "https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a8/lottie.json",
    webp: "https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a8/512.webp",
    gif: "https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a8/512.gif",
    alt: "🚨",
  },
  caution: {
    lottie:
      "https://fonts.gstatic.com/s/e/notoemoji/latest/26a0_fe0f/lottie.json",
    webp: "https://fonts.gstatic.com/s/e/notoemoji/latest/26a0_fe0f/512.webp",
    gif: "https://fonts.gstatic.com/s/e/notoemoji/latest/26a0_fe0f/512.gif",
    alt: "⚠️",
  },
  safe: {
    lottie: "https://fonts.gstatic.com/s/e/notoemoji/latest/2705/lottie.json",
    webp: "https://fonts.gstatic.com/s/e/notoemoji/latest/2705/512.webp",
    gif: "https://fonts.gstatic.com/s/e/notoemoji/latest/2705/512.gif",
    alt: "✅",
  },
};
