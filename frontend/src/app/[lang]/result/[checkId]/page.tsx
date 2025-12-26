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
import { SafetyLevel } from "@/types";
import { getSafetyLevel } from "@/utils/safetyScore";

const LOTTIE_URLS: Record<SafetyLevel, string> = {
  danger: "https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a8/lottie.json",
  caution:
    "https://fonts.gstatic.com/s/e/notoemoji/latest/26a0_fe0f/lottie.json",
  safe: "https://fonts.gstatic.com/s/e/notoemoji/latest/2705/lottie.json",
};

export default function TradeSafetyResultPage() {
  const params = useParams();
  const { t } = useTranslation(TRADE_SAFETY_NS);
  const checkId = Array.isArray(params.checkId)
    ? params.checkId[0]
    : params.checkId;

  const repository = useMemo<TradeSafetyRepository>(
    () => new TradeSafetyRepository(getApiService()),
    [],
  );

  const [result, setResult] =
    useState<TradeSafetyCheckRepositoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lottieData, setLottieData] = useState<object | null>(null);

  // Don't set default "safe" to prevent "Flash of Safe" UX issue
  const safetyLevel = result
    ? getSafetyLevel(result.llm_analysis.safe_score)
    : null;

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

  useEffect(() => {
    // Don't fetch until we have actual safetyLevel (prevents "Flash of Safe")
    if (!safetyLevel) {
      setLottieData(null);
      return;
    }

    let isMounted = true;

    const fetchLottie = async () => {
      try {
        const response = await fetch(LOTTIE_URLS[safetyLevel]);
        if (!response.ok) {
          throw new Error("Failed to fetch Lottie");
        }
        const data = (await response.json()) as object;

        if (isMounted) {
          setLottieData(data);
        }
      } catch (err) {
        if (isMounted) {
          console.error("Failed to load Lottie animation:", err);
          setLottieData(null);
        }
      }
    };

    void fetchLottie();

    return () => {
      isMounted = false;
    };
  }, [safetyLevel]);

  if (isLoading) {
    return (
      <div className="container mx-auto px-6 py-20">
        <div className="flex justify-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  if (error || !result || !safetyLevel) {
    return (
      <div className="container mx-auto px-6 py-20">
        <div className="alert alert-error">
          <span>{error || t("result.notFound")}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-20">
      <div className="mx-auto mb-12 max-w-3xl">
        <PageHeader
          level={safetyLevel}
          score={result.llm_analysis.safe_score}
          lottieData={lottieData}
        />
        <div className="mt-6">
          <DetailedResult analysis={result.llm_analysis} />
        </div>
      </div>
    </div>
  );
}
