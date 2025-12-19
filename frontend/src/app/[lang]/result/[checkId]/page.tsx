"use client";

import { DetailedResult } from "@/components/DetailedResult";
import { SafetyLevel, PageHeader } from "@/components/PageHeader";
import { mockTradeSafetyResult } from "@/mocks/TradeSafetyCheck.mock";

const SAFETY_SCORE_THRESHOLDS = {
  safe: 70,
  caution: 40,
} as const;

const getSafetyLevel = (safetyScore: number): SafetyLevel => {
  if (safetyScore >= SAFETY_SCORE_THRESHOLDS.safe) return "safe";
  if (safetyScore >= SAFETY_SCORE_THRESHOLDS.caution) return "caution";
  return "danger";
};

export default function TradeSafetyResultPage() {
  const result = mockTradeSafetyResult;
  const safetyLevel = getSafetyLevel(result.llm_analysis.safe_score);

  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto mb-12 max-w-3xl">
        <PageHeader
          level={safetyLevel}
          score={result.llm_analysis.safe_score}
        />
        <div className="mt-6">
          <DetailedResult analysis={result.llm_analysis} />
        </div>
      </div>
    </div>
  );
}
