"use client";

import Link from "next/link";
import { useTranslation } from "react-i18next";

import { QuickSummary } from "../types";

interface QuickResultTeaserProps {
  summary: QuickSummary;
  checkId: string;
}

export function QuickResultTeaser({
  summary,
  checkId,
}: QuickResultTeaserProps) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language;

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-8 text-center text-3xl font-bold">
        {t("page.tradeSafety.result.title")}
      </h1>

      {/* Quick Summary Cards */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="card bg-error/10">
          <div className="card-body items-center text-center">
            <h3 className="text-4xl font-bold text-error">
              {summary.risk_signals_count}
            </h3>
            <p className="text-sm">
              {t("page.tradeSafety.result.riskSignals")}
            </p>
          </div>
        </div>
        <div className="card bg-warning/10">
          <div className="card-body items-center text-center">
            <h3 className="text-4xl font-bold text-warning">
              {summary.cautions_count}
            </h3>
            <p className="text-sm">{t("page.tradeSafety.result.cautions")}</p>
          </div>
        </div>
        <div className="card bg-success/10">
          <div className="card-body items-center text-center">
            <h3 className="text-4xl font-bold text-success">
              {summary.safe_indicators_count}
            </h3>
            <p className="text-sm">
              {t("page.tradeSafety.result.safeIndicators")}
            </p>
          </div>
        </div>
      </div>

      {/* Signup Prompt */}
      <div className="card bg-base-200 shadow-xl">
        <div className="card-body items-center text-center">
          <h2 className="card-title text-2xl">
            {t("page.tradeSafety.result.signupRequired")}
          </h2>
          <p className="mb-4 text-neutral-content">
            {t("page.tradeSafety.result.signupMessage")}
          </p>
          <Link
            href={`/${lang}/login?callbackUrl=${encodeURIComponent(`/${lang}/trade-safety/result/${checkId}`)}`}
            className="btn btn-primary"
          >
            {t("login")}
          </Link>
        </div>
      </div>
    </div>
  );
}
