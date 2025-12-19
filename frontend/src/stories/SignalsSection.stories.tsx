import type { Meta, StoryObj } from "@storybook/react";

import type { RiskSignal } from "@/types";

import { SignalsSection } from "../components/DetailedResult/SignalsSection";

const meta: Meta<typeof SignalsSection> = {
  title: "DetailedResult/SignalsSection",
  component: SignalsSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof SignalsSection>;

const mockRiskSignals: RiskSignal[] = [
  {
    category: "content",
    severity: "high",
    title: "Unclear abbreviations and typos",
    description:
      "Some parts of the listing text are unclear. This could indicate a lack of attention to detail.",
    what_to_do:
      "Ask the seller for clarification about unclear terms before proceeding.",
  },
];

const mockCautions: RiskSignal[] = [
  {
    category: "content",
    severity: "medium",
    title: "Meetup location unclear",
    description:
      "The listing mentions a meetup location, but it is unclear where this is.",
    what_to_do:
      "Ensure that the meetup location is a well-lit, public area with lots of people around.",
  },
];

const mockSafeIndicators: RiskSignal[] = [
  {
    category: "seller",
    severity: "low",
    title: "Willing to meet in person",
    description:
      "The seller offers to meet in person, which allows for direct inspection.",
    what_to_do:
      "During the meetup, inspect the items carefully for authenticity before paying.",
  },
];

export const RiskSignals: Story = {
  args: {
    signals: mockRiskSignals,
    variant: "error",
  },
};

export const Cautions: Story = {
  args: {
    signals: mockCautions,
    variant: "warning",
  },
};

export const SafeIndicators: Story = {
  args: {
    signals: mockSafeIndicators,
    variant: "success",
  },
};

export const MultipleSignals: Story = {
  args: {
    signals: [
      ...mockRiskSignals,
      {
        category: "payment",
        severity: "high",
        title: "Suspicious payment method",
        description: "The seller only accepts non-refundable payment methods.",
        what_to_do: "Request a safer payment method with buyer protection.",
      },
    ],
    variant: "error",
  },
};
