import { z } from "zod";

import { BaseCrudRepository } from "@aioia/core";

// Zod schema for nested objects
const riskSignalSchema = z.object({
  category: z.enum(["payment", "seller", "platform", "price", "content"]),
  severity: z.enum(["high", "medium", "low"]),
  title: z.string(),
  description: z.string(),
  what_to_do: z.string(),
});

const priceAnalysisSchema = z
  .object({
    market_price_range: z.string().nullish(),
    offered_price: z.number().nullish(),
    currency: z.string().nullish(),
    price_assessment: z.string(),
    warnings: z.array(z.string()),
  })
  .nullish();

const tradeSafetyAnalysisSchema = z.object({
  translation: z.string().nullish(),
  nuance_explanation: z.string().nullish(),
  risk_signals: z.array(riskSignalSchema),
  cautions: z.array(riskSignalSchema),
  safe_indicators: z.array(riskSignalSchema),
  price_analysis: priceAnalysisSchema,
  safety_checklist: z.array(z.string()),
  risk_score: z.number(),
  recommendation: z.string(),
  emotional_support: z.string(),
});

const quickSummarySchema = z.object({
  risk_signals_count: z.number(),
  cautions_count: z.number(),
  safe_indicators_count: z.number(),
});

const tradeSafetyCheckResponseSchema = z.object({
  id: z.string(),
  user_id: z.string().nullish(),
  input_text: z.string(),
  llm_analysis: tradeSafetyAnalysisSchema,
  risk_score: z.number(),
  expert_advice: z.string().nullish(),
  expert_reviewed: z.boolean(),
  expert_reviewed_at: z.string().nullish(),
  expert_reviewed_by: z.string().nullish(),
  created_at: z.string(),
  updated_at: z.string(),
});

// Full response for authenticated users
export type TradeSafetyCheckFullResponse = z.infer<
  typeof tradeSafetyCheckResponseSchema
>;

// Quick response for non-authenticated users
export interface QuickCheckRepositoryResponse {
  id: string;
  quick_summary: {
    risk_signals_count: number;
    cautions_count: number;
    safe_indicators_count: number;
  };
  signup_required: true;
}

// Union type for repository responses
export type TradeSafetyCheckRepositoryResponse =
  | TradeSafetyCheckFullResponse
  | QuickCheckRepositoryResponse;

// Union schema for repository responses
const tradeSafetyCheckRepositoryResponseSchema = z.union([
  tradeSafetyCheckResponseSchema,
  z.object({
    id: z.string(),
    quick_summary: quickSummarySchema,
    signup_required: z.literal(true),
  }),
]);

export class TradeSafetyRepository extends BaseCrudRepository<TradeSafetyCheckRepositoryResponse> {
  readonly resource = "trade-safety";

  protected getDataSchema() {
    return tradeSafetyCheckRepositoryResponseSchema;
  }
}
