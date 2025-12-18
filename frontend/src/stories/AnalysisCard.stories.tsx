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

export const Error: Story = {
  args: {
    title: "Risk Signal",
    variant: "error",
    children: <p className="text-sm">This indicates a high risk warning.</p>,
  },
};

export const Warning: Story = {
  args: {
    title: "Caution",
    variant: "warning",
    children: <p className="text-sm">This indicates a medium risk caution.</p>,
  },
};

export const Success: Story = {
  args: {
    title: "Safe Indicator",
    variant: "success",
    children: <p className="text-sm">This indicates a safe signal.</p>,
  },
};

export const Info: Story = {
  args: {
    title: "Information",
    variant: "info",
    children: <p className="text-sm">This is an informational card.</p>,
  },
};

export const WithoutTitle: Story = {
  args: {
    variant: "default",
    children: <p className="text-sm">Card without title.</p>,
  },
};
