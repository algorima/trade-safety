import type { Meta, StoryObj } from "@storybook/react";

import { SafetyChecklistSection } from "../components/DetailedResult/SafetyChecklistSection";

const meta: Meta<typeof SafetyChecklistSection> = {
  title: "DetailedResult/SafetyChecklistSection",
  component: SafetyChecklistSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof SafetyChecklistSection>;

export const Default: Story = {
  args: {
    items: [
      "Confirm the exact currency being used",
      "Ask for clear photos of the items with a handwritten date and username",
      "Research the seller's reputation in trading communities",
      "Arrange the meetup in a safe, public place",
      "Bring a friend to the meetup",
    ],
  },
};

export const FewItems: Story = {
  args: {
    items: ["Verify seller identity", "Use secure payment method"],
  },
};
