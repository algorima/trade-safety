import type { Meta, StoryObj } from "@storybook/react";

import { SectionContent } from "../components/DetailedResult/SectionContent";

const meta: Meta<typeof SectionContent> = {
  title: "DetailedResult/SectionContent",
  component: SectionContent,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof SectionContent>;

export const Default: Story = {
  args: {
    title: "Translation",
    content:
      "Want to sell (WTS) and looking for buyers (LFB). Selling Seventeen assorted photocards for 100 each.",
  },
};

export const LongContent: Story = {
  args: {
    title: "What to do",
    content:
      "Ask the seller for clarification about unclear terms before proceeding. Make sure to verify all details and request additional photos if needed. Consider meeting in a public place for in-person transactions.",
  },
};
