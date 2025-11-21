/**
 * Trade Safety React Components
 *
 * AI-powered safety analysis for K-pop merchandise trading
 */

// Components
export { DetailedResult } from "./components/DetailedResult";
export { QuickResultTeaser } from "./components/QuickResultTeaser";
export { RiskSignalCard } from "./components/RiskSignalCard";

// API & Types
export { TradeSafetyRepository } from "./api/repository";
export type * from "./api/types";

// i18n - Export translation objects for integration
export { default as enTranslations } from "./i18n/locales/en/translation.json";
export { default as koTranslations } from "./i18n/locales/ko/translation.json";
export { default as jaTranslations } from "./i18n/locales/ja/translation.json";
export { default as zhTranslations } from "./i18n/locales/zh/translation.json";
export { default as esTranslations } from "./i18n/locales/es/translation.json";
export { default as idTranslations } from "./i18n/locales/id/translation.json";
