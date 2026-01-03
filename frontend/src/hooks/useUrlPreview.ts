import { useCallback, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { TRADE_SAFETY_NS } from "@/i18n";
import type { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import type { LinkPreviewData } from "@/types";
import { detectUrl, mapPostPreviewToLinkPreview } from "@/utils/urlPreview";

export function useUrlPreview(
  inputText: string,
  repository: TradeSafetyRepository,
) {
  const { t } = useTranslation(TRADE_SAFETY_NS);

  const [previewData, setPreviewData] = useState<LinkPreviewData | null>(null);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const lastUrlRef = useRef<string | null>(null);

  const getErrorMessage = useCallback(() => t("hero.previewError"), [t]);

  useEffect(() => {
    const detectedUrl = detectUrl(inputText);

    if (!detectedUrl) {
      setPreviewData(null);
      setPreviewError(null);
      setIsLoadingPreview(false);
      lastUrlRef.current = null;
      return;
    }

    if (lastUrlRef.current === detectedUrl) {
      return;
    }

    const controller = new AbortController();
    const { signal } = controller;

    const timeoutId = setTimeout(() => {
      lastUrlRef.current = detectedUrl;

      const fetchPreview = async () => {
        setIsLoadingPreview(true);
        setPreviewError(null);

        try {
          const postPreview = await repository.fetchPreview(detectedUrl, {
            signal,
          });
          const linkPreviewData = mapPostPreviewToLinkPreview(
            postPreview,
            detectedUrl,
          );
          setPreviewData(linkPreviewData);
        } catch (err) {
          if (err instanceof Error && err.name !== "AbortError") {
            console.error("Failed to fetch URL metadata:", err);
            setPreviewData(null);
            setPreviewError(getErrorMessage());
          }
        } finally {
          if (!signal.aborted) {
            setIsLoadingPreview(false);
          }
        }
      };

      void fetchPreview();
    }, 300);

    return () => {
      clearTimeout(timeoutId);
      controller.abort();
    };
  }, [inputText, repository, getErrorMessage]);

  return { previewData, isLoadingPreview, previewError };
}
