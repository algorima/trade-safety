import type { Meta, StoryObj } from "@storybook/react";

import { PriceAnalysisSection } from "../components/DetailedResult/PriceAnalysisSection";

const meta: Meta<typeof PriceAnalysisSection> = {
  title: "DetailedResult/PriceAnalysisSection",
  component: PriceAnalysisSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof PriceAnalysisSection>;

export const Default: Story = {
  args: {
    data: {
      market_price_range: "₱80-150 PHP per photocard (approx.)",
      offered_price: 100,
      currency: "PHP",
      price_assessment:
        "The price falls within the typical market range for these items.",
      warnings: ["Confirm the item's condition before proceeding."],
    },
  },
};

export const WithUSD: Story = {
  args: {
    data: {
      market_price_range: "$15-30 USD",
      offered_price: 25,
      currency: "USD",
      price_assessment: "The price is within the normal market range.",
      warnings: [],
    },
  },
};

export const WithKRW: Story = {
  args: {
    data: {
      market_price_range: "₩10,000-20,000 KRW",
      offered_price: 15000,
      currency: "KRW",
      price_assessment: "Fair price for this item.",
      warnings: [],
    },
  },
};

export const PartialData: Story = {
  args: {
    data: {
      price_assessment: "Unable to determine exact market price.",
      warnings: ["Price comparison not available for this item."],
    },
  },
};
