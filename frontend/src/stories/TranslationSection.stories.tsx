import type { Meta, StoryObj } from "@storybook/react";

import { TranslationSection } from "../components/DetailedResult/TranslationSection";

const meta: Meta<typeof TranslationSection> = {
  title: "DetailedResult/TranslationSection",
  component: TranslationSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof TranslationSection>;

export const Default: Story = {
  args: {
    translation:
      "Want to sell (WTS) and looking for buyers (LFB). Selling Seventeen assorted photocards for 100 each.",
    nuance:
      "The seller is using K-pop-specific abbreviations. 'WTS' = want to sell, 'LFB' = looking for buyers.",
  },
};

export const TranslationOnly: Story = {
  args: {
    translation:
      "Selling photocard set for $50. Meet up available in downtown area.",
    nuance: null,
  },
};

export const NuanceOnly: Story = {
  args: {
    translation: null,
    nuance:
      "The text contains informal language typical of online marketplaces.",
  },
};
