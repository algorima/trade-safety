import type { Meta, StoryObj } from "@storybook/react";

import { QuickResultTeaser } from "../components/QuickResultTeaser";

const meta: Meta<typeof QuickResultTeaser> = {
  title: "Trade Safety/QuickResultTeaser",
  component: QuickResultTeaser,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const HighRisk: Story = {
  args: {
    summary: {
      risk_signals_count: 5,
      cautions_count: 3,
      safe_indicators_count: 1,
    },
    checkId: "test-check-id-123",
  },
};

export const MediumRisk: Story = {
  args: {
    summary: {
      risk_signals_count: 2,
      cautions_count: 4,
      safe_indicators_count: 3,
    },
    checkId: "test-check-id-456",
  },
};

export const LowRisk: Story = {
  args: {
    summary: {
      risk_signals_count: 0,
      cautions_count: 1,
      safe_indicators_count: 8,
    },
    checkId: "test-check-id-789",
  },
};

export const NoRiskSignals: Story = {
  args: {
    summary: {
      risk_signals_count: 0,
      cautions_count: 0,
      safe_indicators_count: 10,
    },
    checkId: "test-check-id-safe",
  },
};
