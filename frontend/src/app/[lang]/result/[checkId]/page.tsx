"use client";

import { getSafetyLevel } from "@/utils/safetyScore";
import { DetailedResult } from "@/components/DetailedResult";
import { PageHeader } from "@/components/PageHeader";
import { mockTradeSafetyResult } from "@/mocks/TradeSafetyCheck.mock";

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
