"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { PriceAnalysis } from "@/types";

import { AnalysisCard } from "./AnalysisCard";

interface PriceAnalysisSectionProps {
  data?: PriceAnalysis;
}

export function PriceAnalysisSection({ data }: PriceAnalysisSectionProps) {
  const { t, i18n } = useTranslation(TRADE_SAFETY_NS);
  if (!data) return null;

  return (
    <AnalysisCard title={t("result.priceAnalysis")}>
      {data.market_price_range && (
        <div className="mb-2">
          <h3 className="text-sm font-bold">{t("result.marketPrice")}</h3>
          <p className="text-xs">{data.market_price_range}</p>
        </div>
      )}

      {data.offered_price && (
        <div className="mb-2">
          <h3 className="text-sm font-bold"> {t("result.offeredPrice")}</h3>
          <p className="text-xs">
            {new Intl.NumberFormat(i18n.language, {
              style: "currency",
              currency: data.currency || "USD",
            }).format(data.offered_price)}
          </p>
        </div>
      )}

      {data.price_assessment && (
        <div>
          <h3 className="text-sm font-bold"> {t("result.priceAssessment")}</h3>
          <p className="text-xs">{data.price_assessment}</p>
        </div>
      )}
    </AnalysisCard>
  );
}
