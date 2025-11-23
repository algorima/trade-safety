import type { Meta, StoryObj } from "@storybook/react";

import { CautionsSection } from "../components/DetailedResult/CautionsSection";

const meta: Meta<typeof CautionsSection> = {
  title: "Trade Safety/DetailedResult/CautionsSection",
  component: CautionsSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    cautions: [
      {
        category: "platform",
        severity: "medium",
        title: "Unverified Platform",
        description:
          "Trade is happening on a less common platform without buyer protection.",
        what_to_do:
          "Propose moving to a verified marketplace or use a middleman service.",
      },
      {
        category: "seller",
        severity: "medium",
        title: "Limited Reviews",
        description: "Seller has only 2 reviews, both from this month.",
        what_to_do: "Request additional verification and proceed cautiously.",
      },
    ],
  },
};
