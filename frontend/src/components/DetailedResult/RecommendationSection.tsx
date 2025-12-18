"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

interface RecommendationSectionProps {
  recommendation?: string;
}

export function RecommendationSection({
  recommendation,
}: RecommendationSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (!recommendation) return null;

  return (
    <AnalysisCard title={t("result.recommendation")}>
      <p className="text-xs">{recommendation}</p>
    </AnalysisCard>
  );
}
