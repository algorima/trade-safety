"use client";

import { motion, Variants } from "framer-motion";

import { TradeSafetyAnalysis } from "@/types";

import { CautionsSection } from "./CautionsSection";
import { CompanionCtaSection } from "./CompanionCtaSection";
import { ExpertAdviceSection } from "./ExpertAdviceSection";
import { PriceAnalysisSection } from "./PriceAnalysisSection";
import { RecommendationSection } from "./RecommendationSection";
import { RiskScoreHero } from "./RiskScoreHero";
import { RiskSignalsSection } from "./RiskSignalsSection";
import { SafeIndicatorsSection } from "./SafeIndicatorsSection";
import { SafetyChecklistSection } from "./SafetyChecklistSection";
import { TranslationSection } from "./TranslationSection";

interface DetailedResultProps {
  analysis: TradeSafetyAnalysis;
  expertAdvice?: string | null;
}

const fadeInUp: Variants = {
  initial: { y: 40, opacity: 0 },
  animate: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.6 },
  },
};

const staggerContainer: Variants = {
  animate: {
    transition: {
      staggerChildren: 0.15,
    },
  },
};

export function DetailedResult({
  analysis,
  expertAdvice,
}: DetailedResultProps) {
  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="mx-auto max-w-5xl space-y-12"
    >
      {/* Hero: 종합 위험도 */}
      <motion.div variants={fadeInUp}>
        <RiskScoreHero score={analysis.risk_score} />
      </motion.div>

      {/* 번역 + 뉘앙스 */}
      {(analysis.translation || analysis.nuance_explanation) && (
        <motion.div variants={fadeInUp}>
          <TranslationSection
            translation={analysis.translation}
            nuance={analysis.nuance_explanation}
          />
        </motion.div>
      )}

      {/* 위험 신호 */}
      {analysis.risk_signals.length > 0 && (
        <motion.div variants={fadeInUp}>
          <RiskSignalsSection signals={analysis.risk_signals} />
        </motion.div>
      )}

      {/* 주의사항 */}
      {analysis.cautions.length > 0 && (
        <motion.div variants={fadeInUp}>
          <CautionsSection cautions={analysis.cautions} />
        </motion.div>
      )}

      {/* 안전 요소 */}
      {analysis.safe_indicators.length > 0 && (
        <motion.div variants={fadeInUp}>
          <SafeIndicatorsSection indicators={analysis.safe_indicators} />
        </motion.div>
      )}

      {/* 가격 분석 */}
      {analysis.price_analysis && (
        <motion.div variants={fadeInUp}>
          <PriceAnalysisSection data={analysis.price_analysis} />
        </motion.div>
      )}

      {/* 체크리스트 */}
      {analysis.safety_checklist.length > 0 && (
        <motion.div variants={fadeInUp}>
          <SafetyChecklistSection items={analysis.safety_checklist} />
        </motion.div>
      )}

      {/* 전문가 조언 (있을 경우) */}
      {expertAdvice && (
        <motion.div variants={fadeInUp}>
          <ExpertAdviceSection advice={expertAdvice} />
        </motion.div>
      )}

      {/* 종합 추천 */}
      <motion.div variants={fadeInUp}>
        <RecommendationSection
          recommendation={analysis.recommendation}
          emotionalSupport={analysis.emotional_support}
        />
      </motion.div>

      {/* AI 동반자 CTA */}
      <motion.div variants={fadeInUp}>
        <CompanionCtaSection />
      </motion.div>
    </motion.div>
  );
}
