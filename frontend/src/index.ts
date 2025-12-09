/**
 * Trade Safety React Components
 *
 * AI-powered safety analysis for K-pop merchandise trading
 */

// Components
export { DetailedResult } from "./components/DetailedResult";
export { QuickResultTeaser } from "./components/QuickResultTeaser";
export { RiskSignalCard } from "./components/RiskSignalCard";

// Repositories (Repository pattern for API access)
export { TradeSafetyRepository } from "./repositories";
export type {
  TradeSafetyCheckRepositoryResponse,
  TradeSafetyCheckFullResponse,
  QuickCheckRepositoryResponse,
} from "./repositories/TradeSafetyRepository";

// Types & Constants
export * from "./types";

// i18n - Export namespace constant and translations for library integration
export { TRADE_SAFETY_NS } from "./i18n";

import enTranslations from "./i18n/locales/en/tradeSafety.json";
import esTranslations from "./i18n/locales/es/tradeSafety.json";
import idTranslations from "./i18n/locales/id/tradeSafety.json";
import jaTranslations from "./i18n/locales/ja/tradeSafety.json";
import koTranslations from "./i18n/locales/ko/tradeSafety.json";
import zhTranslations from "./i18n/locales/zh/tradeSafety.json";

/**
 * Translation resources for the tradeSafety namespace.
 * Use with i18next.addResourceBundle(lang, 'tradeSafety', translations)
 *
 * @example
 * import { tradeSafetyTranslations, TRADE_SAFETY_NS } from '@trade-safety/react';
 *
 * // Add to existing i18n instance
 * Object.entries(tradeSafetyTranslations).forEach(([lang, resources]) => {
 *   i18n.addResourceBundle(lang, TRADE_SAFETY_NS, resources);
 * });
 */
export const tradeSafetyTranslations = {
  en: enTranslations,
  es: esTranslations,
  id: idTranslations,
  ja: jaTranslations,
  ko: koTranslations,
  zh: zhTranslations,
};
