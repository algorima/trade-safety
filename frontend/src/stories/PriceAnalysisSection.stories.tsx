import type { Meta, StoryObj } from "@storybook/react";

import { PriceAnalysisSection } from "../components/DetailedResult/PriceAnalysisSection";

const meta: Meta<typeof PriceAnalysisSection> = {
  title: "Trade Safety/DetailedResult/PriceAnalysisSection",
  component: PriceAnalysisSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const SuspiciousPrice: Story = {
  args: {
    data: {
      market_price_range: "$50 - $80 USD",
      offered_price: 25,
      currency: "USD",
      price_assessment:
        "The offered price is significantly below market value. This could indicate a counterfeit item or a scam. Proceed with extreme caution.",
      warnings: [
        "Price is 50% below market average",
        "Extremely low price is a red flag",
      ],
    },
  },
};

export const FairPrice: Story = {
  args: {
    data: {
      market_price_range: "$50 - $80 USD",
      offered_price: 65,
      currency: "USD",
      price_assessment:
        "The price is within the normal market range. This is a good sign of a legitimate sale.",
      warnings: [],
    },
  },
};

export const NoOfferedPrice: Story = {
  args: {
    data: {
      market_price_range: "$30 - $50 USD",
      offered_price: null,
      currency: null,
      price_assessment:
        "The seller hasn't listed a specific price. Ask for pricing details before proceeding.",
      warnings: ["No price specified"],
    },
  },
};

export const MarketRangeOnly: Story = {
  args: {
    data: {
      market_price_range: "$100 - $150 USD (rare item)",
      offered_price: null,
      currency: null,
      price_assessment:
        "Market price information only. No specific offer provided.",
      warnings: [],
    },
  },
};

export const HighEndItem: Story = {
  args: {
    data: {
      market_price_range: "$200 - $500 USD",
      offered_price: 350,
      currency: "USD",
      price_assessment:
        "This is a high-value item priced fairly within market range. Ensure you use a secure payment method with buyer protection.",
      warnings: [],
    },
  },
};

export const KoreanWonPrice: Story = {
  args: {
    data: {
      market_price_range: "₩15,000 - ₩20,000 KRW",
      offered_price: 18000,
      currency: "KRW",
      price_assessment:
        "가격이 시장 평균 범위 내에 있습니다. 정상적인 거래로 보입니다.",
      warnings: [],
    },
  },
};
