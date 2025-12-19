import type { Meta, StoryObj } from "@storybook/react";

import { RecommendationSection } from "../components/DetailedResult/RecommendationSection";

const meta: Meta<typeof RecommendationSection> = {
  title: "DetailedResult/RecommendationSection",
  component: RecommendationSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof RecommendationSection>;

export const Default: Story = {
  args: {
    recommendation:
      "Proceed with caution. Ensure you clarify all unclear terms and verify the authenticity of the items before committing to a purchase or trade. Take your time to gather more information.",
  },
};

export const Short: Story = {
  args: {
    recommendation:
      "This transaction appears safe. Proceed with normal caution.",
  },
};
