import { BaseCrudRepository } from "@aioia/core";
import { z } from "zod";

// Zod schema for nested objects
const riskSignalSchema = z.object({
  category: z.enum(["payment", "seller", "platform", "price", "content"]),
  severity: z.enum(["high", "medium", "low"]),
  title: z.string(),
  description: z.string(),
  what_to_do: z.string(),
});

const priceAnalysisSchema = z.object({
  market_price_range: z.string().nullish(),
  offered_price: z.number().nullish(),
  currency: z.string().nullish(),
  price_assessment: z.string(),
  warnings: z.array(z.string()),
});

const tradeSafetyAnalysisSchema = z.object({
  ai_summary: z.array(z.string()),
  translation: z.string().nullish(),
  nuance_explanation: z.string().nullish(),
  risk_signals: z.array(riskSignalSchema),
  cautions: z.array(riskSignalSchema),
  safe_indicators: z.array(riskSignalSchema),
  price_analysis: priceAnalysisSchema,
  safety_checklist: z.array(z.string()),
  safe_score: z.number(),
  recommendation: z.string(),
  emotional_support: z.string(),
});

const tradeSafetyCheckResponseSchema = z.object({
  id: z.string(),
  user_id: z.string().nullish(),
  input_text: z.string(),
  llm_analysis: tradeSafetyAnalysisSchema,
  safe_score: z.number(),
  expert_advice: z.string().nullish(),
  expert_reviewed: z.boolean(),
  expert_reviewed_at: z.string().nullish(),
  expert_reviewed_by: z.string().nullish(),
  created_at: z.string(),
  updated_at: z.string(),
});

// Platform enum for social media platforms
const platformSchema = z.enum(["twitter"]);

// PostPreview schema for social media post metadata
const postPreviewSchema = z.object({
  platform: platformSchema,
  author: z.string(),
  created_at: z.string().nullish(),
  text: z.string(),
  text_preview: z.string(),
  images: z.array(z.string()),
});

// Response wrapper for preview endpoint
const previewResponseSchema = z.object({
  data: postPreviewSchema,
});

// Response type for all users
export type TradeSafetyCheckRepositoryResponse = z.infer<
  typeof tradeSafetyCheckResponseSchema
>;

// PostPreview type
export type PostPreview = z.infer<typeof postPreviewSchema>;

export class TradeSafetyRepository extends BaseCrudRepository<TradeSafetyCheckRepositoryResponse> {
  readonly resource = "trade-safety";

  protected getDataSchema() {
    return tradeSafetyCheckResponseSchema;
  }

  /**
   * Fetch post preview metadata from a social media URL
   * POST /trade-safety/preview
   */
  async fetchPreview(
    url: string,
    fetchOptions?: RequestInit,
  ): Promise<PostPreview> {
    const endpoint = `${this.apiService.buildUrl(this.resource)}/preview`;
    const rawResponse = await this.apiService.request(endpoint, {
      ...fetchOptions,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const validated = this.validateResponse(rawResponse, previewResponseSchema);
    return validated.data;
  }
}
