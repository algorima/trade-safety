"use client";

import clsx from "clsx";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { SafetyLevel } from "@/types";

interface AnalysisCardProps {
  badgeVariant?: SafetyLevel;
  subtitle?: string;
  icon?: React.ReactNode;
  title: string;
  titleSize?: "sm" | "lg";
  children: React.ReactNode;
}

const badgeStyles = {
  danger: "bg-error/10 text-error",
  caution: "bg-error/10 text-error",
  safe: "bg-neutral/10 text-neutral",
};

const badgeLabel = {
  danger: "result.danger.badge",
  caution: "result.caution.badge",
  safe: "result.safe.badge",
};

const titleSizeStyles = {
  sm: "text-xl font-bold",
  lg: "text-2xl font-bold",
};

export function AnalysisCard({
  badgeVariant,
  subtitle,
  icon,
  title,
  titleSize = "lg",
  children,
}: AnalysisCardProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <section className="rounded-2xl bg-neutral-content p-6 shadow-sm">
      <header className="mb-4 flex flex-col items-start">
        {badgeVariant && (
          <div
            className={clsx(
              "mb-2 rounded-full px-4 py-1 text-sm font-bold",
              badgeStyles[badgeVariant],
            )}
          >
            {t(badgeLabel[badgeVariant])}
          </div>
        )}

        {subtitle && (
          <p className="mb-1 break-keep text-lg font-medium text-neutral">
            {subtitle}
          </p>
        )}

        <div className="flex items-center gap-2 text-neutral">
          {icon && <span className="text-base">{icon}</span>}
          <h2
            className={clsx(
              "whitespace-pre-line break-keep sm:whitespace-normal",
              titleSizeStyles[titleSize],
            )}
          >
            {title}
          </h2>
        </div>
      </header>

      <div>{children}</div>
    </section>
  );
}
