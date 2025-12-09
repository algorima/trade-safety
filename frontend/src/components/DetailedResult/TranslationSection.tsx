"use client";

import { LanguageIcon } from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "../../i18n";

interface TranslationSectionProps {
  translation?: string | null;
  nuance?: string | null;
}

export function TranslationSection({
  translation,
  nuance,
}: TranslationSectionProps) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  if (!translation && !nuance) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <LanguageIcon className="size-10 text-primary" />
        {t("result.translation")}
      </h3>

      <div className="card bg-base-200 shadow-xl">
        <div className="card-body">
          {translation && (
            <div className="mb-4">
              <h4 className="mb-2 text-lg font-semibold">
                {t("result.translationTitle")}
              </h4>
              <p className="whitespace-pre-wrap text-neutral-content">
                {translation}
              </p>
            </div>
          )}

          {nuance && (
            <div>
              <h4 className="mb-2 text-lg font-semibold">
                {t("result.nuanceTitle")}
              </h4>
              <p className="whitespace-pre-wrap text-neutral-content">
                {nuance}
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
