"use client";

import clsx from "clsx";
import { useTranslation } from "react-i18next";
import { IoSparkles } from "react-icons/io5";

import { TRADE_SAFETY_NS } from "@/i18n";

import { AnalysisCard } from "./AnalysisCard";

// mock data
const MOCK_SUMMARY_LIST: string[] = [
  "PayPal F&F과 Wise 결제 유도 같은 명확한 위험 패턴 감지",
  "거래 가격은 시세 범위 내에 있어 비교적 안정적",
  "선입금 유도같은 명확한 위험 패턴 감지",
];

interface AISummarySectionProps {
  summary: string;
}

export function AISummarySection({ summary: _summary }: AISummarySectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <AnalysisCard title={t("result.aiSummary")} icon={<IoSparkles />}>
      <div>
        {MOCK_SUMMARY_LIST.map((item, index) => (
          <p
            key={index}
            className={clsx(
              "py-2 text-sm leading-relaxed text-base-content",
              index < MOCK_SUMMARY_LIST.length - 1 &&
                "border-b border-base-300",
            )}
          >
            {item}
          </p>
        ))}
      </div>
    </AnalysisCard>
  );
}
