"use client";

import { TradeSafetyAnalysis } from "@/types";

import { AISummarySection } from "./AISummarySection";
import { PriceAnalysisSection } from "./PriceAnalysisSection";
import { RecommendationSection } from "./RecommendationSection";
import { SafetyChecklistSection } from "./SafetyChecklistSection";
import { SignalsSection } from "./SignalsSection";
import { TranslationSection } from "./TranslationSection";

interface DetailedResultProps {
  analysis: TradeSafetyAnalysis;
}

export function DetailedResult({ analysis }: DetailedResultProps) {
  return (
    <div>
      {analysis.ai_summary && (
        <AISummarySection summary={analysis.ai_summary} />
      )}

      <div className="my-4 flex flex-col gap-4">
        {/* 번역 및 뉘앙스 */}
        {(analysis.translation || analysis.nuance_explanation) && (
          <TranslationSection
            translation={analysis.translation}
            nuance={analysis.nuance_explanation}
          />
        )}

        {/* 가격 분석 */}
        {analysis.price_analysis && (
          <PriceAnalysisSection data={analysis.price_analysis} />
        )}

        {/* 종합 추천 */}
        {analysis.recommendation && (
          <RecommendationSection recommendation={analysis.recommendation} />
        )}
      </div>

      {/* 위험 신호 */}
      {analysis.risk_signals.length > 0 && (
        <SignalsSection signals={analysis.risk_signals} variant="error" />
      )}

      {/* 주의 사항 */}
      {analysis.cautions.length > 0 && (
        <SignalsSection signals={analysis.cautions} variant="warning" />
      )}

      {/* 안전 지표 */}
      {analysis.safe_indicators.length > 0 && (
        <SignalsSection signals={analysis.safe_indicators} variant="success" />
      )}

      {/* 안전 체크리스트 */}
      {analysis.safety_checklist.length > 0 && (
        <SafetyChecklistSection items={analysis.safety_checklist} />
      )}
    </div>
  );
}
