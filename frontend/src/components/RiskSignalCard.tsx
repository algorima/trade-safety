"use client";

import {
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/solid";
import clsx from "clsx";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../i18n";
import { RiskSignal } from "../types";

interface RiskSignalCardProps {
  signal: RiskSignal;
  variant?: "error" | "warning" | "success";
}

const variantStyles = {
  error: "bg-error/10 border-error/30",
  warning: "bg-warning/10 border-warning/30",
  success: "bg-success/10 border-success/30",
};

const iconColor = {
  error: "text-error",
  warning: "text-warning",
  success: "text-success",
};

const severityIcon = {
  high: ExclamationCircleIcon,
  medium: ExclamationTriangleIcon,
  low: InformationCircleIcon,
};

export function RiskSignalCard({
  signal,
  variant = "error",
}: RiskSignalCardProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);
  const Icon = severityIcon[signal.severity];

  return (
    <div className={clsx("card border-2 backdrop-blur-sm", variantStyles[variant])}>
      <div className="card-body">
        <div className="flex items-start gap-4">
          <Icon className={clsx("mt-1 size-8 shrink-0", iconColor[variant])} />

          <div className="flex-1">
            <h4 className="card-title text-xl">{signal.title}</h4>
            <p className="mt-2 text-base-content/70">{signal.description}</p>

            {/* What to do */}
            <div className="mt-4 rounded-lg bg-base-100/50 p-4">
              <p className="mb-2 text-sm font-semibold">
                💡 {t("result.whatToDo")}
              </p>
              <p className="text-sm">{signal.what_to_do}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
