import type { Meta, StoryObj } from "@storybook/react";

import { SafeIndicatorsSection } from "../components/DetailedResult/SafeIndicatorsSection";

const meta: Meta<typeof SafeIndicatorsSection> = {
  title: "Trade Safety/DetailedResult/SafeIndicatorsSection",
  component: SafeIndicatorsSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    indicators: [
      {
        category: "seller",
        severity: "low",
        title: "Verified Seller",
        description: "Seller has 50+ positive reviews spanning 2 years.",
        what_to_do: "This is a good sign, but still verify item authenticity.",
      },
      {
        category: "content",
        severity: "low",
        title: "Detailed Photos",
        description:
          "Post includes multiple high-quality photos from various angles.",
        what_to_do:
          "Good transparency - still ask for dated authentication photos.",
      },
      {
        category: "payment",
        severity: "low",
        title: "Secure Payment Offered",
        description:
          "Seller accepts PayPal Goods & Services with buyer protection.",
        what_to_do: "Perfect! This protects your purchase.",
      },
    ],
  },
};
