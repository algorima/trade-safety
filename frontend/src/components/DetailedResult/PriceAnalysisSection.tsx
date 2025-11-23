"use client";

import {
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { PriceAnalysis } from "../../types";

interface PriceAnalysisSectionProps {
  data?: PriceAnalysis;
}

export function PriceAnalysisSection({ data }: PriceAnalysisSectionProps) {
  const { t, i18n } = useTranslation();

  if (!data) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <CurrencyDollarIcon className="size-10 text-secondary" />
        {t("page.tradeSafety.result.priceAnalysis")}
      </h3>

      <div className="card bg-base-200 shadow-xl">
        <div className="card-body">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            {data.market_price_range && (
              <div>
                <h4 className="mb-2 text-lg font-semibold">
                  {t("page.tradeSafety.result.marketPrice")}
                </h4>
                <p className="text-2xl font-bold">{data.market_price_range}</p>
              </div>
            )}

            {data.offered_price && (
              <div>
                <h4 className="mb-2 text-lg font-semibold">
                  {t("page.tradeSafety.result.offeredPrice")}
                </h4>
                <p className="text-2xl font-bold text-primary">
                  {new Intl.NumberFormat(i18n.language, {
                    style: "currency",
                    currency: data.currency || "USD",
                  }).format(data.offered_price)}
                </p>
              </div>
            )}
          </div>

          {/* Price Assessment */}
          <div className="mt-6 rounded-lg bg-base-100 p-4">
            <h4 className="mb-2 text-lg font-semibold">
              {t("page.tradeSafety.result.priceAssessment")}
            </h4>
            <p className="text-neutral-content">{data.price_assessment}</p>
          </div>

          {/* Warnings */}
          {data.warnings.length > 0 && (
            <div className="mt-4">
              <h4 className="mb-2 flex items-center gap-2 text-lg font-semibold text-warning">
                <ExclamationTriangleIcon className="size-6" />
                {t("page.tradeSafety.result.priceWarnings")}
              </h4>
              <ul className="list-inside list-disc space-y-1">
                {data.warnings.map((warning, index) => (
                  <li key={index} className="text-neutral-content">
                    {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
