import type { Meta, StoryObj } from "@storybook/react";

import { RiskSignalCard } from "../components/RiskSignalCard";

const meta: Meta<typeof RiskSignalCard> = {
  title: "Trade Safety/RiskSignalCard",
  component: RiskSignalCard,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const ErrorVariant: Story = {
  args: {
    variant: "error",
    signal: {
      category: "payment",
      severity: "high",
      title: "Suspicious Payment Method",
      description:
        "The seller requests payment through an untraceable method like gift cards or cryptocurrency.",
      what_to_do:
        "Only use secure payment methods with buyer protection like PayPal Goods & Services.",
    },
  },
};

export const WarningVariant: Story = {
  args: {
    variant: "warning",
    signal: {
      category: "seller",
      severity: "medium",
      title: "New Seller Account",
      description:
        "The seller's account was created recently with no transaction history.",
      what_to_do:
        "Request additional verification and check for reviews in K-pop communities.",
    },
  },
};

export const SuccessVariant: Story = {
  args: {
    variant: "success",
    signal: {
      category: "platform",
      severity: "low",
      title: "Verified Platform",
      description:
        "The seller is using a well-known and trusted K-pop marketplace with buyer protection.",
      what_to_do: "Proceed with confidence but still verify item authenticity.",
    },
  },
};

export const LongContent: Story = {
  args: {
    variant: "error",
    signal: {
      category: "content",
      severity: "high",
      title: "Missing Critical Information",
      description:
        "The trade post lacks essential details such as item condition, shipping method, expected delivery time, return policy, and authentication photos. This is a major red flag as legitimate sellers typically provide comprehensive information to build trust with buyers. The absence of these details suggests the seller may be hiding something or is not serious about the transaction.",
      what_to_do:
        "Request all missing information before proceeding. Ask for: 1) Multiple high-quality photos from different angles, 2) Photos with today's date and seller's username, 3) Clear shipping and return policies, 4) Estimated delivery timeline, 5) Payment method details with buyer protection. If the seller refuses to provide these, walk away from the deal immediately.",
    },
  },
};
