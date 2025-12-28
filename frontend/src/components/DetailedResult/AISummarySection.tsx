"use client";

import { SparklesIcon } from "@heroicons/react/24/solid";
import clsx from "clsx";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

interface AISummarySectionProps {
  summary: string[];
}

export function AISummarySection({ summary }: AISummarySectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (summary.length === 0) return null;

  return (
    <AnalysisCard
      title={t("result.aiSummary")}
      icon={<SparklesIcon className="size-6" />}
    >
      <div>
        {summary.map((item, index) => (
          <p
            key={`${item}-${index}`}
            className={clsx(
              "py-2 text-sm leading-relaxed text-neutral",
              index < summary.length - 1 && "border-b border-base-300",
            )}
          >
            {item}
          </p>
        ))}
      </div>
    </AnalysisCard>
  );
}
