import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import type { LinkPreviewData } from "@/components/UrlPreviewCard";
import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";
import { detectUrl, mapPostPreviewToLinkPreview } from "@/utils/urlPreview";

export function useUrlPreview(inputText: string) {
  const { t } = useTranslation(TRADE_SAFETY_NS);
  const repository = useMemo<TradeSafetyRepository>(
    () => new TradeSafetyRepository(getApiService()),
    [],
  );

  const [previewData, setPreviewData] = useState<LinkPreviewData | null>(null);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const lastUrlRef = useRef<string | null>(null);

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
        const postPreview = await repository.fetchPreview(detectedUrl);
        const linkPreviewData = mapPostPreviewToLinkPreview(
          postPreview,
          detectedUrl,
        );

        if (!isCancelled) {
          setPreviewData(linkPreviewData);
        }
      } catch (err) {
        if (!isCancelled) {
          console.error("Failed to fetch URL metadata:", err);
          setPreviewData(null);
          setPreviewError(t("hero.previewError"));
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
    // repository is stable (created with useMemo and empty deps)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inputText]);

  return { previewData, isLoadingPreview, previewError };
}
