import type { Meta, StoryObj } from "@storybook/react";

import { RiskScoreHero } from "../components/DetailedResult/RiskScoreHero";

const meta: Meta<typeof RiskScoreHero> = {
  title: "Trade Safety/DetailedResult/RiskScoreHero",
  component: RiskScoreHero,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const HighRisk: Story = {
  args: {
    score: 85,
  },
};

export const MediumRisk: Story = {
  args: {
    score: 55,
  },
};

export const LowRisk: Story = {
  args: {
    score: 25,
  },
};

export const VeryHighRisk: Story = {
  args: {
    score: 95,
  },
};

export const VerySafe: Story = {
  args: {
    score: 10,
  },
};
