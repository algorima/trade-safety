"use client";

import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { DetailedResult } from "@/components/DetailedResult";
import { PageHeader } from "@/components/PageHeader";
import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories";
import { TradeSafetyCheckRepositoryResponse } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";
import { getSafetyLevel } from "@/utils/safetyScore";

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
    if (typeof checkId !== "string" || !checkId) {
      setError("Analysis Not found");
      setIsLoading(false);
      return;
    }

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

  const safetyLevel = getSafetyLevel(result.llm_analysis.safe_score);

  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto mb-12 max-w-3xl">
        <PageHeader
          level={safetyLevel}
          score={result.llm_analysis.safe_score}
        />
        <div className="mt-6">
          <DetailedResult analysis={result.llm_analysis} />
        </div>
      </div>
    </div>
  );
}
