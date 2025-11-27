import type { Meta, StoryObj } from "@storybook/react";

import { TranslationSection } from "../components/DetailedResult/TranslationSection";

const meta: Meta<typeof TranslationSection> = {
  title: "Trade Safety/DetailedResult/TranslationSection",
  component: TranslationSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const WithBoth: Story = {
  args: {
    translation: "I'm selling a limited edition BTS photocard. DM for price!",
    nuance:
      "The casual tone and abbreviations (DM) are common in K-pop trading communities. However, not listing the price upfront is a minor red flag.",
  },
};

export const TranslationOnly: Story = {
  args: {
    translation:
      "Selling SEVENTEEN photocard set from latest album. Mint condition, never opened.",
    nuance: null,
  },
};

export const NuanceOnly: Story = {
  args: {
    translation: null,
    nuance:
      "The seller uses very polite Korean (존댓말) which is standard in trading communities and shows professionalism.",
  },
};

export const LongText: Story = {
  args: {
    translation:
      "Hello everyone! I'm looking to sell my entire K-pop collection as I'm moving abroad next month. This includes photocards, albums, official lightsticks, and other merchandise from various groups including BTS, BLACKPINK, TWICE, and SEVENTEEN. Everything is in excellent condition and I can provide photos upon request. I'm open to negotiations and bundle deals. Please send me a direct message if you're interested!",
    nuance:
      "This is a very detailed and professional post. The seller explains the reason for selling (moving abroad), which adds credibility. The mention of 'bundle deals' and 'negotiations' is common in K-pop communities. The use of formal language and complete sentences suggests a serious, trustworthy seller. However, the lack of specific pricing is still something to note.",
  },
};
