import type { TradeSafetyCheckResponse } from "@/types";

export const mockTradeSafetyResult: TradeSafetyCheckResponse = {
  id: "mock-check-id",
  user_id: null,
  input_text:
    "WTS/LFB Seventeen assorted photocards 100 each. 2:1 to Doremiz for JH/WW/MG. WTT/LFT SVT items. Meetup AMMB Saturday. fts fml dagat burstday heaven. PayPal F&F only, no refunds.",
  safe_score: 85,
  expert_advice: null,
  expert_reviewed: false,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),

  llm_analysis: {
    ai_summary:
      "The listing is for selling and trading Seventeen photocards, with specific trade ratios mentioned. The seller is looking to meet at a location abbreviated as AMMB on Saturday. The text includes several abbreviations common in K-pop trading communities, but also contains some unclear terms that may need clarification.",
    translation:
      "Want to sell (WTS) and looking for buyers (LFB). Selling Seventeen assorted photocards for 100 each (currency not specified). If you're getting Jeonghan (JH), Wonwoo (WW), or Mingyu (MG), the trade ratio is 2:1 for Doremiz (likely referring to a specific photocard set). Can meet up at AMMB (likely a location abbreviation) on Saturday. Want to trade (WTT) and looking for trade (LFT) for Seventeen stuff (likely merchandise). The rest of the text ('fts fml dagat burstday heaven') appears to be a mix of slang, typos, or references that are unclear.",

    nuance_explanation:
      "The seller is using a mix of K-pop-specific abbreviations and possibly some typos. Key terms: 'WTS' = want to sell, 'LFB' = looking for buyers, 'WTT' = want to trade, 'LFT' = looking for trade. '2:1 to Doremiz' likely suggests a trade ratio of 2:1 in favor of a specific photocard set. 'AMMB' could be a location abbreviation (e.g., a mall or station). The final part of the text ('fts fml dagat burstday heaven') could be slang, typos, or references to other items for sale or trade, but they are unclear and lack context.",

    safe_score: 85,

    risk_signals: [
      {
        category: "content",
        severity: "high",
        title: "Unclear abbreviations and typos",
        description:
          "Some parts of the listing text ('fts fml dagat burstday heaven') are unclear. This could indicate a lack of attention to detail or potentially confuse buyers about what is being sold or traded.",
        what_to_do:
          "Ask the seller for clarification about unclear terms and ensure you fully understand what is being offered before proceeding.",
      },
    ],

    cautions: [
      {
        category: "content",
        severity: "medium",
        title: "Meetup location",
        description:
          "The listing mentions 'AMMB' as a meetup location, but it is unclear where or what this is. If it is a public place, it may be safe, but if it's a private or remote area, it could pose a risk.",
        what_to_do:
          "Ensure that the meetup location is a well-lit, public area with lots of people around. Bring a friend if possible.",
      },
    ],

    safe_indicators: [
      {
        category: "seller",
        severity: "low",
        title: "Willing to meet in person",
        description:
          "The seller offers to meet in person, which can allow for direct inspection of the items before payment.",
        what_to_do:
          "During the meetup, inspect the photocards carefully for authenticity and condition before paying.",
      },
    ],

    price_analysis: {
      market_price_range: "₱80-150 PHP per photocard (approx.)",
      offered_price: 100,
      currency: "PHP",
      price_assessment:
        "The price of 100 PHP per photocard falls within the typical market range for Seventeen photocards, depending on rarity and demand.",
      warnings: [
        "The price is within the typical market range, but confirm the card's condition and authenticity before proceeding.",
      ],
    },

    safety_checklist: [
      "Confirm the exact currency being used",
      "Ask for clear photos of the photocards with a handwritten date and username for authentication.",
      "Verify the rarity or set ('Doremiz') mentioned in the trade ratio.",
      "Research the seller's reputation in K-pop trading communities or ask for references.",
      "Arrange the meetup in a safe, public place and bring a friend.",
    ],

    recommendation:
      "Proceed with caution. Ensure you clarify all unclear terms and verify the authenticity of the items before committing to a purchase or trade. It's okay to take your time to clarify details and make sure you feel comfortable before proceeding. Don't let FOMO pressure you into rushing—there will always be other opportunities to collect your favorite Seventeen photocards!",

    emotional_support:
      "Don't worry! Take your time to gather more information, and I'll be here to help you make a safe and informed decision.",
  },
};
