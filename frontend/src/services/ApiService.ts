import { BaseApiService } from "@aioia/core";

/**
 * API Service for Trade Safety standalone app
 * No authentication required for public trade safety checks
 */
export class ApiService extends BaseApiService {
  constructor() {
    super(process.env.NEXT_PUBLIC_API_BASE_URL);
  }

  /**
   * No authentication headers for public API
   */
  protected getAuthHeaders(): Record<string, string> {
    return {
      "Content-Type": "application/json",
    };
  }

  /**
   * Handle API errors
   */
  protected async handleError(response: Response): Promise<never> {
    const text = await response.text();
    let message = `API Error: ${response.status}`;

    try {
      const json = JSON.parse(text) as { detail?: string };
      if (json.detail) {
        message = json.detail;
      }
    } catch {
      // Use status text if JSON parsing fails
      if (text) {
        message = text;
      }
    }

    throw new Error(message);
  }
}

// Singleton instance
let apiServiceInstance: ApiService | null = null;

export const getApiService = (): ApiService => {
  if (!apiServiceInstance) {
    apiServiceInstance = new ApiService();
  }
  return apiServiceInstance;
};
