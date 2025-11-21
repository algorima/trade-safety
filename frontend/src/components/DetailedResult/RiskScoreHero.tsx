"use client";

import {
  CheckBadgeIcon,
  ExclamationTriangleIcon,
  ShieldExclamationIcon,
} from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

interface RiskScoreHeroProps {
  score: number;
}

interface RiskLevel {
  level: "high" | "medium" | "low";
  color: string;
  Icon: React.ComponentType<{ className?: string }>;
}

function getRiskLevel(score: number): RiskLevel {
  if (score >= 70) {
    return { level: "high", color: "error", Icon: ShieldExclamationIcon };
  }
  if (score >= 40) {
    return { level: "medium", color: "warning", Icon: ExclamationTriangleIcon };
  }
  return { level: "low", color: "success", Icon: CheckBadgeIcon };
}

export function RiskScoreHero({ score }: RiskScoreHeroProps) {
  const { t } = useTranslation();
  const risk = getRiskLevel(score);
  const { Icon } = risk;

  const colorClasses: Record<string, string> = {
    error: "text-error",
    warning: "text-warning",
    success: "text-success",
  };

  return (
    <div className="hero min-h-[40vh] rounded-3xl bg-base-200">
      <div className="hero-content text-center">
        <div>
          <div className="mb-4">
            <Icon className={`size-32 ${colorClasses[risk.color]}`} />
          </div>
          <h2 className="mb-4 text-5xl font-bold">
            {t(`page.tradeSafety.result.riskLevel.${risk.level}.title`)}
          </h2>

          {/* 위험도 게이지 */}
          <div className="mx-auto w-64">
            <div
              className={`radial-progress ${colorClasses[risk.color]}`}
              style={
                {
                  "--value": score,
                  "--size": "12rem",
                  "--thickness": "1rem",
                } as React.CSSProperties
              }
              role="progressbar"
            >
              <span className="text-5xl font-bold">{score}</span>
            </div>
          </div>

          <p className="mt-6 max-w-lg text-xl text-neutral-content">
            {t(`page.tradeSafety.result.riskLevel.${risk.level}.message`)}
          </p>
        </div>
      </div>
    </div>
  );
}
