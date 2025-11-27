import type { Meta, StoryObj } from "@storybook/react";

import { SafetyChecklistSection } from "../components/DetailedResult/SafetyChecklistSection";

const meta: Meta<typeof SafetyChecklistSection> = {
  title: "Trade Safety/DetailedResult/SafetyChecklistSection",
  component: SafetyChecklistSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    items: [
      "Request clear photos with today's date and seller's username",
      "Verify seller's reputation in K-pop trading communities",
      "Use PayPal Goods & Services for buyer protection",
      "Never send payment via gift cards or cryptocurrency",
      "Ask about return policy before purchasing",
    ],
  },
};

export const ShortList: Story = {
  args: {
    items: [
      "Verify item authenticity",
      "Use secure payment method",
      "Check seller reviews",
    ],
  },
};

export const LongList: Story = {
  args: {
    items: [
      "Request multiple high-quality photos from different angles",
      "Ask for authentication photos with today's date and seller's username visible",
      "Search for the seller's username in K-pop trading communities (Reddit, Discord, Twitter)",
      "Verify the seller's transaction history and feedback",
      "Only use payment methods with buyer protection (PayPal Goods & Services, eBay)",
      "Never pay with gift cards, cryptocurrency, or direct bank transfers",
      "Ask about shipping method, tracking, and insurance",
      "Clarify the return and refund policy before payment",
      "Request a video of the item if possible",
      "Take your time - don't rush due to FOMO or urgency tactics",
    ],
  },
};
