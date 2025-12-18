"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

interface TranslationSectionProps {
  translation?: string | null;
  nuance?: string | null;
}

export function TranslationSection({
  translation,
  nuance,
}: TranslationSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <AnalysisCard title={t("result.translation")}>
      {translation && (
        <div className="mb-2">
          <h3 className="text-sm font-bold">{t("result.translationTitle")}</h3>
          <p className="text-xs">{translation}</p>
        </div>
      )}

      {nuance && (
        <div>
          <h3 className="text-sm font-bold">{t("result.nuanceTitle")}</h3>
          <p className="text-xs">{nuance}</p>
        </div>
      )}
    </AnalysisCard>
  );
}
