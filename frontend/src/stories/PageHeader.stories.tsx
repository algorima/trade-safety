import type { Meta, StoryObj } from "@storybook/react";

import { PageHeader } from "../components/PageHeader";

const meta: Meta<typeof PageHeader> = {
  title: "Components/PageHeader",
  component: PageHeader,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof PageHeader>;

export const Safe: Story = {
  args: {
    level: "safe",
    score: 70,
  },
};

export const Caution: Story = {
  args: {
    level: "caution",
    score: 40,
  },
};

export const Danger: Story = {
  args: {
    level: "danger",
    score: 39,
  },
};
