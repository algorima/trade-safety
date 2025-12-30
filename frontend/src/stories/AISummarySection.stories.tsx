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
    summary: [
      "PayPal F&F과 Wise 결제 유도 같은 명확한 위험 패턴 감지",
      "거래 가격은 시세 범위 내에 있어 비교적 안정적",
      "선입금 유도 같은 명확한 위험 패턴이 있어 주의 필요",
    ],
  },
};

export const Empty: Story = {
  args: {
    summary: [],
  },
};

export const SingleItem: Story = {
  args: {
    summary: ["거래 가격은 시세 범위 내에 있어 비교적 안정적"],
  },
};

export const TwoItems: Story = {
  args: {
    summary: [
      "PayPal F&F과 Wise 결제 유도 같은 명확한 위험 패턴 감지",
      "거래 가격은 시세 범위 내에 있어 비교적 안정적",
    ],
  },
};
