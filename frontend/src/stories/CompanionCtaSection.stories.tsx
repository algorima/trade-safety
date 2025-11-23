import type { Meta, StoryObj } from "@storybook/react";

import { CompanionCtaSection } from "../components/DetailedResult/CompanionCtaSection";

const meta: Meta<typeof CompanionCtaSection> = {
  title: "Trade Safety/DetailedResult/CompanionCtaSection",
  component: CompanionCtaSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
