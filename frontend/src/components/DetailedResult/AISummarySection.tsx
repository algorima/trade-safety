"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";

interface AISummarySectionProps {
  summary: string;
}

export function AISummarySection({ summary }: AISummarySectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  // Split summary into lines (max 3)
  const lines = summary
    .split("\n")
    .filter((line) => line.trim())
    .slice(0, 3);

  return (
    <div className="mb-6">
      {/* Title with icon */}
      <h2 className="mb-4 flex items-center gap-2 text-lg font-bold text-base-content">
        <span>⚡</span>
        <span>{t("result.aiSummary")}</span>
      </h2>

      {/* 3-line summary list */}
      <ul className="space-y-2">
        {lines.map((line, index) => (
          <li
            key={index}
            className="flex gap-3 text-sm leading-relaxed text-base-content"
          >
            <span className="mt-1.5 size-1 shrink-0 rounded-full bg-base-content"></span>
            <span>{line}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
