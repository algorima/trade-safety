import {
  createInstance,
  CallbackError,
  ResourceKey,
  InitOptions,
  i18n,
  Resource,
} from "i18next";
import resourcesToBackend from "i18next-resources-to-backend";
import { initReactI18next } from "react-i18next/initReactI18next";

import { fallbackLng } from "./config";

/**
 * i18n 인스턴스를 설정하는 공통 함수
 */
const setupI18nInstance = (initialResources?: Resource): i18n => {
  const instance = createInstance();

  // React i18next 초기화
  instance.use(initReactI18next);

  // 초기 리소스가 없는 경우에만 동적 리소스 로딩 추가
  if (!initialResources) {
    instance.use(
      resourcesToBackend(
        (
          language: string,
          namespace: string,
          callback: (
            error: CallbackError | null,
            result: ResourceKey | null,
          ) => void,
        ) => {
          void import(`./locales/${language}/${namespace}.json`)
            .then((resources: ResourceKey) => {
              callback(null, resources);
            })
            .catch((error: Error) => {
              callback(error, null);
            });
        },
      ),
    );
  }

  return instance;
};

/**
 * 기본 i18n 설정 옵션
 */
const getDefaultOptions = (
  lang: string,
  resources?: Resource,
): InitOptions => ({
  lng: lang,
  fallbackLng,
  debug: false,
  interpolation: {
    escapeValue: false,
  },
  resources,
});

/**
 * 비동기적으로 i18n 인스턴스를 생성하고 초기화하는 함수
 * await로 완전히 초기화될 때까지 기다려야 함
 */
export const createI18nInstance = async (
  lang: string,
  initialResources?: Resource,
): Promise<i18n> => {
  const instance = setupI18nInstance(initialResources);

  // 비동기적으로 초기화하고 완료될 때까지 기다림
  await instance.init({
    ...getDefaultOptions(lang, initialResources),
    initImmediate: true, // 비동기 로드 활성화
  });

  return instance;
};

/**
 * 동기적으로 i18n 인스턴스를 생성하는 함수
 * 참고: 동기 초기화를 위해서는 리소스가 필수입니다.
 */
export const createClientI18nInstance = (
  lang: string,
  initialResources: Resource,
): i18n => {
  const instance = setupI18nInstance(initialResources);

  // 동기적으로 초기화하고 promise는 void 처리
  void instance.init({
    ...getDefaultOptions(lang, initialResources),
    initImmediate: false, // 클라이언트에서는 동기 초기화
  });

  return instance;
};

/**
 * 서버 컴포넌트에서 번역 리소스를 로드하는 함수
 * 비동기적으로 초기화하여 모든 리소스 로드
 */
export const getServerTranslationResources = async (
  lang: string,
): Promise<{ resources: Resource }> => {
  // 임시 i18n 인스턴스를 생성하여 리소스만 로드
  const instance = await createI18nInstance(lang);

  // 임시 인스턴스에서 리소스 데이터만 추출
  return {
    resources: { [lang]: instance.services.resourceStore.data[lang] },
  };
};
