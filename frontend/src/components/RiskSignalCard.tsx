"use client";

import {
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { RiskSignal } from "@/types";

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
  const { t } = useTranslation();
  const Icon = severityIcon[signal.severity];

  return (
    <div className={`card ${variantStyles[variant]} border-2 backdrop-blur-sm`}>
      <div className="card-body">
        <div className="flex items-start gap-4">
          <Icon className={`size-8 ${iconColor[variant]} mt-1 shrink-0`} />

          <div className="flex-1">
            <h4 className="card-title text-xl">{signal.title}</h4>
            <p className="mt-2 text-neutral-content">{signal.description}</p>

            {/* What to do */}
            <div className="mt-4 rounded-lg bg-base-100/50 p-4">
              <p className="mb-2 text-sm font-semibold">
                💡 {t("page.tradeSafety.result.whatToDo")}
              </p>
              <p className="text-sm">{signal.what_to_do}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
