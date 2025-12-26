"use client";

import Lottie from "lottie-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { SafetyLevel } from "@/types";

interface PageHeaderProps {
  level: SafetyLevel;
  score: number;
}

const LOTTIE_URLS: Record<SafetyLevel, string> = {
  danger:
    "https://raw.githubusercontent.com/googlefonts/noto-emoji-animation/main/json/emoji_u1f6a8.json",
  caution:
    "https://raw.githubusercontent.com/googlefonts/noto-emoji-animation/main/json/emoji_u26a0.json",
  safe: "https://raw.githubusercontent.com/googlefonts/noto-emoji-animation/main/json/emoji_u2705.json",
};

const LEVEL_COLORS: Record<SafetyLevel, { text: string; bg: string }> = {
  danger: { text: "text-error", bg: "bg-error/10" },
  caution: { text: "text-warning", bg: "bg-warning/10" },
  safe: { text: "text-success", bg: "bg-success/10" },
};

export function PageHeader({ level, score }: PageHeaderProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);
  const [lottieData, setLottieData] = useState<object | null>(null);

  useEffect(() => {
    const fetchLottie = async () => {
      try {
        const response = await fetch(LOTTIE_URLS[level]);
        const data = (await response.json()) as object;
        setLottieData(data);
      } catch (error) {
        console.error("Failed to load Lottie animation:", error);
      }
    };

    void fetchLottie();
  }, [level]);

  const colors = LEVEL_COLORS[level];

  return (
    <div className="mb-8 flex flex-col items-center text-center">
      {/* Badge */}
      <div className="mb-4 rounded-full bg-base-300 px-4 py-1.5">
        <span className="text-sm font-medium text-base-content">
          {t(`result.safetyLevel.${level}.badge`)}
        </span>
      </div>

      {/* Title */}
      <h1 className="mb-6 text-2xl font-bold leading-tight sm:text-3xl md:text-4xl">
        <span className="text-base-content">
          {t(`result.safetyLevel.${level}.prefix`)}
        </span>
        <br className="sm:hidden" />
        <span className={`${colors.text} ml-0 sm:ml-2`}>
          {t(`result.safetyLevel.${level}.suffix`)}
        </span>
      </h1>

      {/* Lottie Icon */}
      <div className="mb-6 flex size-32 items-center justify-center sm:size-40 md:size-48">
        {lottieData ? (
          <Lottie animationData={lottieData} loop autoplay />
        ) : (
          <div className="loading loading-spinner loading-lg"></div>
        )}
      </div>

      {/* Description */}
      <p className="max-w-md whitespace-pre-line text-sm leading-relaxed text-base-content/80 sm:text-base">
        {t(`result.safetyLevel.${level}.description`, { score })}
      </p>
    </div>
  );
}
