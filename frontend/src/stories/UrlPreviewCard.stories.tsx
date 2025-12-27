import type { Meta, StoryObj } from "@storybook/react";

import {
  type LinkPreviewData,
  UrlPreviewCard,
} from "../components/UrlPreviewCard";
import { MOCK_REDDIT_PREVIEW, MOCK_TWITTER_PREVIEW } from "../utils/urlPreview";

const meta: Meta<typeof UrlPreviewCard> = {
  title: "Trade Safety/UrlPreviewCard",
  component: UrlPreviewCard,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
  decorators: [
    (Story) => (
      <div className="mx-auto max-w-2xl bg-base-100 p-4">
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

const singleImageData: LinkPreviewData = {
  url: "https://x.com/user/status/789",
  title: "Important security announcement about phishing attempts",
  author: "@security_team",
  date: "2024-03-16",
  content: "Please be aware of recent phishing attempts...",
  images: ["https://picsum.photos/seed/security1/800/600"],
};

const noImagesData: LinkPreviewData = {
  url: "https://reddit.com/r/scams/comments/xyz",
  title: "PSA: How to identify common online scams",
  author: "u/helpful_moderator",
  date: "2024-03-13",
  content:
    "Here's a comprehensive guide to spotting scams online. Please share!",
  images: [],
};

export const TwitterPost: Story = {
  args: {
    data: MOCK_TWITTER_PREVIEW,
  },
};

export const RedditPost: Story = {
  args: {
    data: MOCK_REDDIT_PREVIEW,
  },
};

export const WithSingleImage: Story = {
  args: {
    data: singleImageData,
  },
};

export const WithTwoImages: Story = {
  args: {
    data: {
      ...MOCK_REDDIT_PREVIEW,
      images: [
        "https://picsum.photos/seed/two1/800/600",
        "https://picsum.photos/seed/two2/800/600",
      ],
    },
  },
};

export const WithThreeImages: Story = {
  args: {
    data: MOCK_TWITTER_PREVIEW,
  },
};

export const NoImages: Story = {
  args: {
    data: noImagesData,
  },
};

export const LongTitle: Story = {
  args: {
    data: {
      ...MOCK_TWITTER_PREVIEW,
      title:
        "This is a very long title that demonstrates how the component handles exceptionally long titles that might wrap to multiple lines in the preview card interface",
    },
  },
};

export const LongAuthorName: Story = {
  args: {
    data: {
      ...MOCK_REDDIT_PREVIEW,
      author: "u/this_is_a_very_long_username_that_should_be_handled_properly",
    },
  },
};
