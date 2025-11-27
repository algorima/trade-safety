"use client";

import { LanguageIcon } from "@heroicons/react/24/solid";
import { useTranslation } from "react-i18next";

interface TranslationSectionProps {
  translation?: string | null;
  nuance?: string | null;
}

export function TranslationSection({
  translation,
  nuance,
}: TranslationSectionProps) {
  const { t } = useTranslation();

  if (!translation && !nuance) return null;

  return (
    <section>
      <h3 className="mb-6 flex items-center gap-3 text-3xl font-bold">
        <LanguageIcon className="size-10 text-primary" />
        {t("page.tradeSafety.result.translation")}
      </h3>

      <div className="card bg-base-200 shadow-xl">
        <div className="card-body">
          {translation && (
            <div className="mb-4">
              <h4 className="mb-2 text-lg font-semibold">
                {t("page.tradeSafety.result.translationTitle")}
              </h4>
              <p className="whitespace-pre-wrap text-neutral-content">
                {translation}
              </p>
            </div>
          )}

          {nuance && (
            <div>
              <h4 className="mb-2 text-lg font-semibold">
                {t("page.tradeSafety.result.nuanceTitle")}
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
