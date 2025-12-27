"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { HomeHeroSection } from "@/components/HomeHeroSection";
import type { LinkPreviewData } from "@/components/UrlPreviewCard";
import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";
import { detectUrl, fetchUrlMetadata } from "@/utils/urlPreview";

export default function HomePage() {
  const { i18n } = useTranslation(TRADE_SAFETY_NS);
  const router = useRouter();

  const repository = useMemo<TradeSafetyRepository>(
    () => new TradeSafetyRepository(getApiService()),
    [],
  );

  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewData, setPreviewData] = useState<LinkPreviewData | null>(null);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const lastUrlRef = useRef<string | null>(null);

  // URL 감지 및 미리보기 데이터 페칭
  useEffect(() => {
    const detectedUrl = detectUrl(inputText);

    if (!detectedUrl) {
      setPreviewData(null);
      setPreviewError(null);
      lastUrlRef.current = null;
      return;
    }

    if (lastUrlRef.current === detectedUrl) {
      return;
    }

    lastUrlRef.current = detectedUrl;
    let isCancelled = false;

    const fetchPreview = async () => {
      setIsLoadingPreview(true);
      setPreviewError(null);

      try {
        const metadata = await fetchUrlMetadata(detectedUrl);

        if (!isCancelled) {
          setPreviewData(metadata);
        }
      } catch (err) {
        if (!isCancelled) {
          console.error("Failed to fetch URL metadata:", err);
          setPreviewData(null);
          setPreviewError("URL 미리보기를 불러올 수 없습니다.");
        }
      } finally {
        if (!isCancelled) {
          setIsLoadingPreview(false);
        }
      }
    };

    void fetchPreview();

    return () => {
      isCancelled = true;
    };
  }, [inputText]);

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const textToAnalyze = previewData?.content || inputText;
      const imageUrls =
        previewData?.images && previewData.images.length > 0
          ? previewData.images
          : undefined;

      const response = await repository.create({
        variables: {
          input_text: textToAnalyze,
          output_language: i18n.language,
          image_urls: imageUrls,
        },
      });

      router.push(`/${i18n.language}/result/${response.data.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-dvh w-full flex-col items-center justify-center bg-base-100 p-6 pt-20 lg:pt-0">
      <HomeHeroSection
        value={inputText}
        onChange={setInputText}
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={error}
        previewData={previewData}
        isLoadingPreview={isLoadingPreview}
        previewError={previewError}
      />
    </main>
  );
}
