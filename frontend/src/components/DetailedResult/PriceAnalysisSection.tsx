"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { PriceAnalysis } from "@/types";

import { AnalysisCard } from "./AnalysisCard";
import { SectionContent } from "./SectionContent";

interface PriceAnalysisSectionProps {
  data?: PriceAnalysis;
}

export function PriceAnalysisSection({ data }: PriceAnalysisSectionProps) {
  const { t, i18n } = useTranslation(TRADE_SAFETY_NS);
  if (!data) return null;

  return (
    <AnalysisCard
      subtitle={t("result.priceAnalysis.subtitle")}
      title={t("result.priceAnalysis.title")}
    >
      <div className="space-y-4">
        {data.market_price_range && (
          <SectionContent
            title={t("result.marketPrice")}
            content={data.market_price_range}
          />
        )}

        {data.offered_price && (
          <SectionContent
            title={t("result.offeredPrice")}
            content={new Intl.NumberFormat(i18n.language, {
              style: "currency",
              currency: data.currency || "USD",
            }).format(data.offered_price)}
          />
        )}

        {data.price_assessment && (
          <SectionContent
            title={t("result.priceAssessment")}
            content={data.price_assessment}
          />
        )}
      </div>
    </AnalysisCard>
  );
}
