import type { Meta, StoryObj } from "@storybook/react";

import { ExpertAdviceSection } from "../components/DetailedResult/ExpertAdviceSection";

const meta: Meta<typeof ExpertAdviceSection> = {
  title: "Trade Safety/DetailedResult/ExpertAdviceSection",
  component: ExpertAdviceSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    advice:
      "Based on my experience with K-pop trading, this seller's pattern matches known scam tactics. I've seen similar cases where sellers rush buyers and disappear after payment. Please be very careful.",
  },
};

export const Positive: Story = {
  args: {
    advice:
      "I recognize this seller from verified K-pop trading communities. They have a solid reputation and have completed many successful transactions. You're in good hands!",
  },
};

export const LongAdvice: Story = {
  args: {
    advice:
      "This is a complex situation that requires extra attention. The seller's post has some concerning elements, but they might just be inexperienced rather than malicious. Here's what I recommend:\n\n1. Ask the seller to provide their username on known K-pop trading platforms\n2. Request to see their previous transaction confirmations\n3. Propose using a middleman service if the amount is significant\n4. Take screenshots of all communications\n\nIf the seller cooperates with these requests, you can proceed. If they resist or make excuses, that's a major red flag and you should walk away.",
  },
};
