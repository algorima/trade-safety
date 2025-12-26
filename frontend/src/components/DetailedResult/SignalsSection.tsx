"use client";

import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { RiskSignal, SafetyLevel } from "@/types";

import { AnalysisCard } from "./AnalysisCard";
import { SectionContent } from "./SectionContent";

interface SignalsSectionProps {
  signals: RiskSignal[];
  variant: SafetyLevel;
}

const variantTitle = {
  danger: "result.danger.title",
  caution: "result.caution.title",
  safe: "result.safe.title",
};

export function SignalsSection({ signals, variant }: SignalsSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (signals.length === 0) return null;

  return (
    <AnalysisCard badgeVariant={variant} title={t(variantTitle[variant])}>
      <div className="space-y-4">
        {signals.map((signal, idx) => (
          <div key={idx} className="space-y-4">
            <SectionContent title={signal.title} content={signal.description} />
            <SectionContent
              title={t("result.whatToDo")}
              content={signal.what_to_do}
            />
            {idx < signals.length - 1 && (
              <hr className="mt-4 border-base-300" />
            )}
          </div>
        ))}
      </div>
    </AnalysisCard>
  );
}
