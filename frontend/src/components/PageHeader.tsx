"use client";

import Lottie from "lottie-react";
import { ReactNode } from "react";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { SafetyLevel } from "@/types";

export interface PageHeaderProps {
  level: SafetyLevel;
  score: number;
  lottieData: object | null;
}

interface EmojiAssets {
  lottie: string;
  webp: string;
  gif: string;
  alt: string;
}

const EMOJI_ASSETS: Record<SafetyLevel, EmojiAssets> = {
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

const LEVEL_STYLES: Record<SafetyLevel, string> = {
  danger: "font-bold text-error",
  caution: "font-bold text-warning",
  safe: "font-bold text-success",
};

const parseTextWithBold = (text: string, level: SafetyLevel): ReactNode[] => {
  const parts = text.split(/(<b>.*?<\/b>)/g);

  return parts.map((part, index) => {
    const boldMatch = part.match(/<b>(.*?)<\/b>/);
    if (boldMatch) {
      return (
        <strong key={index} className={LEVEL_STYLES[level]}>
          {boldMatch[1]}
        </strong>
      );
    }
    return part || null;
  });
};

export function PageHeader({ level, score, lottieData }: PageHeaderProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  const assets = EMOJI_ASSETS[level];

  const title = t(`result.safetyLevel.${level}.title`);
  const description = t(`result.safetyLevel.${level}.description`, { score });

  return (
    <div className="mb-8 flex flex-col items-center text-center">
      <div className="mb-4 rounded-full bg-base-300 px-4 py-1.5">
        <span className="text-sm font-medium text-base-content">
          {t(`result.safetyLevel.${level}.badge`)}
        </span>
      </div>

      <h1 className="mb-6 text-4xl font-bold leading-tight text-base-content">
        {parseTextWithBold(title, level)}
      </h1>

      <div className="mb-6 flex size-32 items-center justify-center sm:size-40 md:size-48">
        {lottieData ? (
          <Lottie animationData={lottieData} loop autoplay />
        ) : (
          <picture>
            <source srcSet={assets.webp} type="image/webp" />
            <img
              src={assets.gif}
              alt={assets.alt}
              className="size-full object-contain"
            />
          </picture>
        )}
      </div>

      <p className="max-w-md text-sm leading-relaxed text-base-content/80 sm:text-base">
        {parseTextWithBold(description, level)}
      </p>
    </div>
  );
}
