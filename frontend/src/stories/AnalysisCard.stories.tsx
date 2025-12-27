import { ListBulletIcon } from "@heroicons/react/24/solid";
import type { Meta, StoryObj } from "@storybook/react";

import { AnalysisCard } from "../components/DetailedResult/AnalysisCard";

const meta: Meta<typeof AnalysisCard> = {
  title: "DetailedResult/AnalysisCard",
  component: AnalysisCard,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof AnalysisCard>;

export const Default: Story = {
  args: {
    title: "Default Card",
    children: <p className="text-sm">This is a default card content.</p>,
  },
};

export const Danger: Story = {
  args: {
    title: "Risk Signal",
    badgeVariant: "danger",
    children: <p className="text-sm">This indicates a high risk warning.</p>,
  },
};

export const Caution: Story = {
  args: {
    title: "Caution",
    badgeVariant: "caution",
    children: <p className="text-sm">This indicates a medium risk caution.</p>,
  },
};

export const Safe: Story = {
  args: {
    title: "Safe Indicator",
    badgeVariant: "safe",
    children: <p className="text-sm">This indicates a safe signal.</p>,
  },
};

export const WithSubtitle: Story = {
  args: {
    subtitle: "All terms explained simply",
    title: "Here's what\nthe post means",
    children: <p className="text-sm">Translation content goes here.</p>,
  },
};

export const SmallTitle: Story = {
  args: {
    title: "Checklist",
    titleSize: "sm",
    children: <p className="text-sm">Checklist items go here.</p>,
  },
};

export const WithIcon: Story = {
  args: {
    icon: <ListBulletIcon className="size-6" />,
    title: "Checklist",
    titleSize: "sm",
    children: <p className="text-sm">Checklist items with icon go here.</p>,
  },
};
