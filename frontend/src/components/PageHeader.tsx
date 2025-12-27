"use client";

import Lottie from "lottie-react";
import { Trans, useTranslation } from "react-i18next";

import { EMOJI_ASSETS } from "@/constants/assets";
import { TRADE_SAFETY_NS } from "@/i18n";
import { SafetyLevel } from "@/types";

export interface PageHeaderProps {
  level: SafetyLevel;
  score: number;
  lottieData: object | null;
}

const LEVEL_STYLES: Record<SafetyLevel, string> = {
  danger: "font-bold text-error",
  caution: "font-bold text-warning",
  safe: "font-bold text-success",
};

export function PageHeader({ level, score, lottieData }: PageHeaderProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  const assets = EMOJI_ASSETS[level];

  return (
    <div className="mb-8 flex flex-col items-center text-center">
      <div className="mb-5 rounded-full bg-neutral/75 px-4 py-1.5">
        <span className="text-sm font-medium text-neutral-content">
          {t(`result.safetyLevel.${level}.badge`)}
        </span>
      </div>

      <h1 className="mb-9 break-keep text-4xl font-bold leading-tight text-base-content">
        <Trans
          t={t}
          i18nKey={`result.safetyLevel.${level}.title`}
          components={[<strong key="0" className={LEVEL_STYLES[level]} />]}
        />
      </h1>

      <div className="mb-9 flex size-32 items-center justify-center">
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

      <p className="max-w-md break-keep text-xl leading-relaxed text-base-content">
        <Trans
          t={t}
          i18nKey={`result.safetyLevel.${level}.description`}
          values={{ score }}
          components={[
            <strong key="0" className={LEVEL_STYLES[level]} />,
            <strong key="1" className={LEVEL_STYLES[level]} />,
          ]}
        />
      </p>
    </div>
  );
}
