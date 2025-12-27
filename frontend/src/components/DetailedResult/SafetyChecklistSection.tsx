"use client";

import { ListBulletIcon } from "@heroicons/react/24/solid";
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
    <AnalysisCard
      icon={<ListBulletIcon className="size-6" />}
      title={t("result.safetyChecklist")}
      titleSize="sm"
    >
      <div className="space-y-4">
        {items.map((item, idx) => (
          <label
            key={idx}
            className="label cursor-pointer gap-4 rounded-2xl bg-base-200 p-4"
          >
            <span className="label-text break-keep text-neutral">{item}</span>
            <input
              type="checkbox"
              className="checkbox checkbox-sm [--chkbg:theme(colors.neutral)] [--chkfg:theme(colors.neutral-content)]"
            />
          </label>
        ))}
      </div>
    </AnalysisCard>
  );
}
