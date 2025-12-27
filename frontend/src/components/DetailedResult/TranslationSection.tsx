"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";
import { SectionContent } from "./SectionContent";

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
    <AnalysisCard
      subtitle={t("result.translation.subtitle")}
      title={t("result.translation.title")}
    >
      <div className="space-y-4">
        {translation && (
          <SectionContent
            title={t("result.translation.label")}
            content={translation}
          />
        )}

        {nuance && (
          <SectionContent title={t("result.nuance.label")} content={nuance} />
        )}
      </div>
    </AnalysisCard>
  );
}
