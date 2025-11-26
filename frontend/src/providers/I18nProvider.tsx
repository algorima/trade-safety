"use client";

import { i18n as I18nInstanceType, Resource } from "i18next";
import { ReactNode, useEffect, useRef } from "react";
import { I18nextProvider } from "react-i18next";

import { createClientI18nInstance } from "@/i18n";

interface I18nProviderProps {
  children: ReactNode;
  lang: string;
  resources: Resource;
}

/**
 * 서버 사이드 렌더링과 클라이언트 하이드레이션 간의 일관성을 유지하는 I18n Provider
 * 서버에서 로드한 리소스를 사용하여 동기적으로 초기화합니다.
 */
export function I18nProvider({ children, lang, resources }: I18nProviderProps) {
  // useRef를 사용하여 i18n 인스턴스 저장
  const i18nInstanceRef = useRef<I18nInstanceType | null>(null);

  // 초기에 동기적으로 인스턴스 생성 (서버와 일관성 유지)
  if (!i18nInstanceRef.current) {
    i18nInstanceRef.current = createClientI18nInstance(lang, resources);
  }

  // 언어 변경 시 인스턴스 재초기화를 위한 useEffect
  useEffect(() => {
    // 언어가 변경된 경우에만 인스턴스 재생성
    if (i18nInstanceRef.current?.language !== lang) {
      i18nInstanceRef.current = createClientI18nInstance(lang, resources);
    }
  }, [lang, resources]);

  // 항상 I18nextProvider를 사용하여 하이드레이션 불일치 방지
  return (
    <I18nextProvider i18n={i18nInstanceRef.current}>{children}</I18nextProvider>
  );
}
