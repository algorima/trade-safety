"use client";

import { HeartIcon, LightBulbIcon } from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../../i18n";

interface RecommendationSectionProps {
  recommendation: string;
  emotionalSupport: string;
}

export function RecommendationSection({
  recommendation,
  emotionalSupport,
}: RecommendationSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <LightBulbIcon className="size-10 text-warning" />
        {t("result.recommendation")}
      </h3>

      <div className="card bg-base-200 shadow-xl">
        <div className="card-body">
          <div className="prose max-w-none">
            <p className="whitespace-pre-wrap text-lg text-neutral-content">
              {recommendation}
            </p>
          </div>

          <div className="divider"></div>

          <div className="rounded-lg bg-base-100 p-4">
            <p className="flex items-center gap-2 text-lg font-medium">
              <HeartIcon className="size-6 text-info" /> {emotionalSupport}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
