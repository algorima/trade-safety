"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

interface AISummarySectionProps {
  summary: string;
}

export function AISummarySection({ summary }: AISummarySectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <AnalysisCard title={t("result.aiSummary")}>
      <p className="rounded-lg bg-base-200 p-6 text-sm leading-relaxed text-base-content">
        {summary}
      </p>
    </AnalysisCard>
  );
}
