"use client";

import { useRouter } from "next/navigation";
import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import type { TradeSafetyCheckRepositoryResponse } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";

const isQuickCheckResponse = (
  data: TradeSafetyCheckRepositoryResponse,
): data is Extract<
  TradeSafetyCheckRepositoryResponse,
  { signup_required: true }
> => {
  return "signup_required" in data;
};

export default function HomePage() {
  const { t, i18n } = useTranslation(TRADE_SAFETY_NS);
  const router = useRouter();

  const repository = useMemo<TradeSafetyRepository>(
    () => new TradeSafetyRepository(getApiService()),
    [],
  );

  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await repository.create({
        variables: { input_text: inputText, output_language: i18n.language },
      });

      if (isQuickCheckResponse(response.data)) {
        router.push(`/${i18n.language}/result/${response.data.id}?quick=true`);
      } else {
        router.push(`/${i18n.language}/result/${response.data.id}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto max-w-4xl text-center">
        <h1 className="mb-4 text-4xl font-bold">{t("hero.title")}</h1>
        <p className="mb-8 text-xl text-base-content/70">
          {t("hero.subtitle")}
        </p>

        <div className="card bg-base-200 shadow-xl">
          <div className="card-body">
            <textarea
              id="trade-input"
              className="textarea textarea-bordered h-48 w-full"
              placeholder={t("hero.placeholder")}
              aria-label={t("hero.title")}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={isLoading}
            />

            {error && (
              <div className="alert alert-error mt-4">
                <span>{error}</span>
              </div>
            )}

            <button
              className="btn btn-primary btn-lg mt-4"
              onClick={handleSubmit}
              disabled={isLoading || !inputText.trim()}
            >
              {isLoading ? t("hero.analyzing") : t("hero.checkSafety")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
