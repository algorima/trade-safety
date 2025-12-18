"use client";

import { CheckBadgeIcon } from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

interface SafetyChecklistSectionProps {
  items: string[];
}

export function SafetyChecklistSection({ items }: SafetyChecklistSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (items.length === 0) return null;

  return (
    <div className="mb-4">
      <h2 className="flex items-center gap-1 py-4 font-bold">
        {t("result.safetyChecklist")} <CheckBadgeIcon className="size-6" />
      </h2>
      <AnalysisCard variant="info">
        {items.map((item, idx) => (
          <label key={idx} className="label w-fit cursor-pointer gap-2">
            <input
              type="checkbox"
              className="checkbox rounded-full [--chkbg:theme(colors.neutral)] [--chkfg:theme(colors.neutral-content)]"
            />
            <span className="label-text">{item}</span>
          </label>
        ))}
      </AnalysisCard>
    </div>
  );
}
