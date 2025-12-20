import type { Meta, StoryObj } from "@storybook/react";

import { AISummarySection } from "../components/DetailedResult/AISummarySection";

const meta: Meta<typeof AISummarySection> = {
  title: "DetailedResult/AISummarySection",
  component: AISummarySection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof AISummarySection>;

export const Default: Story = {
  args: {
    summary:
      "This trade appears generally safe. The seller provides clear descriptions with detailed photos, and the price is reasonable for the market. However, we recommend verifying in person before completing the transaction.",
  },
};
