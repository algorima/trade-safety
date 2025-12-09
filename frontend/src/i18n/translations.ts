/**
 * Server-safe exports for trade-safety translations.
 *
 * This module exports only JSON resources and constants,
 * avoiding React-specific code that would break SSR.
 */

import en from "./locales/en/tradeSafety.json";
import es from "./locales/es/tradeSafety.json";
import id from "./locales/id/tradeSafety.json";
import ja from "./locales/ja/tradeSafety.json";
import ko from "./locales/ko/tradeSafety.json";
import zh from "./locales/zh/tradeSafety.json";

/** Trade Safety namespace */
export const TRADE_SAFETY_NS = "tradeSafety";

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
  en,
  es,
  id,
  ja,
  ko,
  zh,
};
