"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { SafetyLevel } from "@/types";

export interface PageHeaderProps {
  level: SafetyLevel;
  score: number;
}

export function PageHeader({ level, score }: PageHeaderProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <div className={"mb-4 rounded-lg"}>
      <h1 className={"mb-2 text-3xl font-bold"}>
        {t(`result.safetyLevel.${level}.title`)}
      </h1>
      <p className="mt-2 text-sm text-neutral">
        {t(`result.safetyLevel.${level}.description`, { score })}
      </p>
    </div>
  );
}
