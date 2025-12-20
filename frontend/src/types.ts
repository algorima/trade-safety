export type RiskSeverity = "high" | "medium" | "low";
export type RiskCategory =
  | "payment"
  | "seller"
  | "platform"
  | "price"
  | "content";

export type SafetyLevel = "safe" | "caution" | "danger";

export const SAFETY_SCORE_THRESHOLDS = {
  safe: 70,
  caution: 40,
} as const;

export interface TradeSafetyCheckRequest {
  input_text: string;
  output_language?: string;
}

export interface RiskSignal {
  category: RiskCategory;
  severity: RiskSeverity;
  title: string;
  description: string;
  what_to_do: string;
}

export interface PriceAnalysis {
  market_price_range?: string | null;
  offered_price?: number | null;
  currency?: string | null;
  price_assessment: string;
  warnings: string[];
}

export interface TradeSafetyAnalysis {
  ai_summary: string;
  translation?: string | null;
  nuance_explanation?: string | null;
  risk_signals: RiskSignal[];
  cautions: RiskSignal[];
  safe_indicators: RiskSignal[];
  price_analysis: PriceAnalysis;
  safety_checklist: string[];
  safe_score: number;
  recommendation: string;
  emotional_support: string;
}

export interface QuickSummary {
  risk_signals_count: number;
  cautions_count: number;
  safe_indicators_count: number;
}

export interface TradeSafetyCheckResponse {
  id: string;
  user_id?: string | null;
  input_text: string;
  llm_analysis: TradeSafetyAnalysis;
  safe_score: number;
  expert_advice?: string | null;
  expert_reviewed: boolean;
  expert_reviewed_at?: string | null;
  expert_reviewed_by?: string | null;
  created_at: string;
  updated_at: string;
}

export interface QuickCheckResponse {
  id: string;
  quick_summary: QuickSummary;
  signup_required: true;
}

export interface TradeSafetyEditFormData {
  expert_advice?: string | null;
  expert_reviewed: boolean;
}
