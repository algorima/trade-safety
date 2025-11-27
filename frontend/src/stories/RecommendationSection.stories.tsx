import type { Meta, StoryObj } from "@storybook/react";

import { RecommendationSection } from "../components/DetailedResult/RecommendationSection";

const meta: Meta<typeof RecommendationSection> = {
  title: "Trade Safety/DetailedResult/RecommendationSection",
  component: RecommendationSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const AvoidTrade: Story = {
  args: {
    recommendation:
      "We strongly recommend NOT proceeding with this trade. Multiple red flags suggest a high risk of fraud.",
    emotionalSupport:
      "It's completely okay to walk away from a trade that feels unsafe. Your safety and peace of mind are more important than any photocard. There will always be other opportunities!",
  },
};

export const ProceedWithCaution: Story = {
  args: {
    recommendation:
      "You can proceed with this trade, but please be extra cautious. Verify all details and use secure payment methods.",
    emotionalSupport:
      "Trust your instincts! If something feels off, it's okay to ask more questions or take your time. A legitimate seller will understand your concerns.",
  },
};

export const SafeToProceed: Story = {
  args: {
    recommendation:
      "This trade appears safe to proceed. The seller shows good signs of legitimacy and transparency.",
    emotionalSupport:
      "Great find! While this looks promising, still follow best practices for online trading. Stay excited but stay safe!",
  },
};
