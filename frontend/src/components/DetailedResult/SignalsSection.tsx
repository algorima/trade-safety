"use client";

import {
  ExclamationTriangleIcon,
  FaceFrownIcon,
  ShieldExclamationIcon,
} from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { RiskSignal } from "@/types";

import { AnalysisCard } from "./AnalysisCard";

interface SignalsSectionProps {
  signals: RiskSignal[];
  variant?: "error" | "warning" | "success";
}

const severityIcon = {
  error: FaceFrownIcon,
  warning: ExclamationTriangleIcon,
  success: ShieldExclamationIcon,
};

const severityTitle = {
  error: "result.riskSignals",
  warning: "result.cautions",
  success: "result.safeIndicators",
};

export function SignalsSection({
  signals,
  variant = "error",
}: SignalsSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (signals.length === 0) return null;

  const Icon = severityIcon[variant];

  return (
    <div className="mb-4">
      <h2 className="flex items-center gap-1 py-4 font-bold">
        {t(severityTitle[variant])} <Icon className="size-6" />
      </h2>
      <div className="space-y-3">
        {signals.map((signal, idx) => (
          <AnalysisCard key={idx} variant={variant}>
            <div className="space-y-2">
              <div>
                <h3 className="text-sm font-bold">{signal.title}</h3>
                <p className="text-xs">{signal.description}</p>
              </div>
              <div>
                <h3 className="text-sm font-bold">{t("result.whatToDo")}</h3>
                <p className="text-xs">{signal.what_to_do}</p>
              </div>
            </div>
          </AnalysisCard>
        ))}
      </div>
    </div>
  );
}
