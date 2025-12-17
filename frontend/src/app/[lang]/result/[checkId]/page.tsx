"use client";

import { useParams } from "next/navigation";
import { useMemo, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import type { TradeSafetyCheckRepositoryResponse } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";

export default function TradeSafetyResultPage() {
  const params = useParams();
  const { t } = useTranslation(TRADE_SAFETY_NS);
  const checkId = params.checkId as string;

  const repository = useMemo<TradeSafetyRepository>(
    () => new TradeSafetyRepository(getApiService()),
    [],
  );

  const [result, setResult] =
    useState<TradeSafetyCheckRepositoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const response = await repository.getOne({ id: checkId });
        setResult(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    void fetchResult();
  }, [checkId, repository]);

  if (isLoading) {
    return (
      <div className="container mx-auto px-6 py-20">
        <div className="flex justify-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="container mx-auto px-6 py-20">
        <div className="alert alert-error">
          <span>{error || t("result.notFound")}</span>
        </div>
      </div>
    );
  }

  // Detailed result
  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto mb-12 max-w-4xl text-center">
        <h1 className="mb-4 text-4xl font-bold">{t("result.title")}</h1>
        <p className="text-xl text-base-content/70">{t("result.subtitle")}</p>
      </div>
    </div>
  );
}
