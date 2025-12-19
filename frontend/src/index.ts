/**
 * Trade Safety React Components
 *
 * AI-powered safety analysis for K-pop merchandise trading
 */

// Components
export { DetailedResult } from "./components/DetailedResult";
export { HomeHeroSection } from "./components/HomeHeroSection";
export type { HomeHeroSectionProps } from "./components/HomeHeroSection";

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
// Note: These exports are from a server-safe module (no React dependencies)
export { TRADE_SAFETY_NS, tradeSafetyTranslations } from "./i18n/translations";
