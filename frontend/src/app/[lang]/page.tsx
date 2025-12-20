"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { HomeHeroSection } from "@/components/HomeHeroSection";
import { TRADE_SAFETY_NS } from "@/i18n";
import { TradeSafetyRepository } from "@/repositories/TradeSafetyRepository";
import { getApiService } from "@/services/ApiService";

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
      />
    </main>
  );
}
