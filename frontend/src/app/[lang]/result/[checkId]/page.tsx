"use client";

import { DetailedResult } from "@/components/DetailedResult";
import { mockTradeSafetyResult } from "@/mocks/TradeSafetyCheck.mock";

export default function TradeSafetyResultPage() {
  const result = mockTradeSafetyResult;

  // Detailed result
  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto mb-12 max-w-3xl">
        <DetailedResult analysis={result.llm_analysis} />
      </div>
    </div>
  );
}
