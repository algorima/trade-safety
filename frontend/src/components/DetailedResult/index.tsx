"use client";

import { TradeSafetyAnalysis } from "@/types";

import { AISummarySection } from "./AISummarySection";
import { PriceAnalysisSection } from "./PriceAnalysisSection";
import { SafetyChecklistSection } from "./SafetyChecklistSection";
import { SignalsSection } from "./SignalsSection";
import { TranslationSection } from "./TranslationSection";

interface DetailedResultProps {
  analysis: TradeSafetyAnalysis;
}

export function DetailedResult({ analysis }: DetailedResultProps) {
  return (
    <div className="space-y-6">
      {analysis.ai_summary.length > 0 && (
        <AISummarySection summary={analysis.ai_summary} />
      )}

      {/* 위험 신호 */}
      {analysis.risk_signals.length > 0 && (
        <SignalsSection signals={analysis.risk_signals} variant="danger" />
      )}

      {/* 주의 사항 */}
      {analysis.cautions.length > 0 && (
        <SignalsSection signals={analysis.cautions} variant="caution" />
      )}

      {/* 안전 지표 */}
      {analysis.safe_indicators.length > 0 && (
        <SignalsSection signals={analysis.safe_indicators} variant="safe" />
      )}

      {/* 안전 체크리스트 */}
      {analysis.safety_checklist.length > 0 && (
        <SafetyChecklistSection items={analysis.safety_checklist} />
      )}

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
    </div>
  );
}
