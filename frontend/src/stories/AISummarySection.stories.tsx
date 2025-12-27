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
    summary: "", // Currently using internal mock data (string[])
  },
};
