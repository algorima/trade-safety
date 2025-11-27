import type { Meta, StoryObj } from "@storybook/react";

import { RiskSignalsSection } from "../components/DetailedResult/RiskSignalsSection";

const meta: Meta<typeof RiskSignalsSection> = {
  title: "Trade Safety/DetailedResult/RiskSignalsSection",
  component: RiskSignalsSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const MultipleSignals: Story = {
  args: {
    signals: [
      {
        category: "payment",
        severity: "high",
        title: "Suspicious Payment Request",
        description: "Seller asks for gift cards or cryptocurrency payment.",
        what_to_do:
          "Only use PayPal Goods & Services or similar protected methods.",
      },
      {
        category: "seller",
        severity: "high",
        title: "Brand New Account",
        description: "Account created less than 24 hours ago with no history.",
        what_to_do:
          "Avoid dealing with brand new accounts for high-value items.",
      },
      {
        category: "content",
        severity: "medium",
        title: "Vague Description",
        description:
          "Post lacks specific details about item condition and shipping.",
        what_to_do: "Request detailed information before proceeding.",
      },
    ],
  },
};

export const SingleSignal: Story = {
  args: {
    signals: [
      {
        category: "price",
        severity: "high",
        title: "Too Good to Be True Price",
        description:
          "The price is 70% below typical market value for this rare item.",
        what_to_do:
          "Extremely suspicious - likely a scam or counterfeit. Walk away.",
      },
    ],
  },
};
