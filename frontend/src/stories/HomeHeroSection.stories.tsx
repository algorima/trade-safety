import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";

import { HomeHeroSection } from "../components/HomeHeroSection";
import { MOCK_REDDIT_PREVIEW, MOCK_TWITTER_PREVIEW } from "../utils/urlPreview";

const meta: Meta<typeof HomeHeroSection> = {
  title: "Trade Safety/HomeHeroSection",
  component: HomeHeroSection,
  tags: ["autodocs"],
  parameters: {
    layout: "padded",
  },
  decorators: [
    (Story) => (
      <div className="flex min-h-dvh w-full flex-col items-center justify-center bg-base-100">
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

const defaultArgs = {
  value: "",
  onChange: fn(),
  onSubmit: fn(),
  isLoading: false,
  error: null,
  previewData: null,
  isLoadingPreview: false,
  previewError: null,
};

export const Default: Story = {
  args: defaultArgs,
};

export const WithText: Story = {
  args: {
    ...defaultArgs,
    value:
      "I'm selling a MacBook Pro 2021 for $1,200. Contact me at email@example.com",
  },
};

export const Loading: Story = {
  args: {
    ...defaultArgs,
    value:
      "I'm selling a MacBook Pro 2021 for $1,200. Contact me at email@example.com",
    isLoading: true,
  },
};

export const WithError: Story = {
  args: {
    ...defaultArgs,
    value: "Short text",
    error: "Failed to analyze the text. Please try again.",
  },
};

export const LongText: Story = {
  args: {
    ...defaultArgs,
    value: `I'm selling a brand new iPhone 14 Pro Max 256GB in Space Black.
The phone is completely sealed and comes with Apple's 1-year warranty.
I bought it last week but received a work phone, so I don't need it anymore.

Price: $1,100 (negotiable)
Location: Downtown Seattle
Contact: john.doe@email.com or (555) 123-4567

Serious buyers only. Cash or Venmo accepted.
Can meet at Apple Store for verification.

Additional details:
- 256GB storage
- Space Black color
- Factory sealed
- Full warranty included
- Original receipt available
- No trades, cash only
- Available for immediate pickup`,
  },
};

export const MobileView: Story = {
  args: {
    ...defaultArgs,
    value:
      "I'm selling a MacBook Pro 2021 for $1,200. Contact me at email@example.com",
  },
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
  },
};

export const TabletView: Story = {
  args: {
    ...defaultArgs,
    value:
      "I'm selling a MacBook Pro 2021 for $1,200. Contact me at email@example.com",
  },
  parameters: {
    viewport: {
      defaultViewport: "tablet",
    },
  },
};

export const WithTwitterPreview: Story = {
  args: {
    ...defaultArgs,
    value: "Check out this post: https://x.com/crypto_expert/status/123456",
    previewData: MOCK_TWITTER_PREVIEW,
  },
};

export const WithRedditPreview: Story = {
  args: {
    ...defaultArgs,
    value: "https://reddit.com/r/security/comments/abc123",
    previewData: MOCK_REDDIT_PREVIEW,
  },
};

export const LoadingPreview: Story = {
  args: {
    ...defaultArgs,
    value: "https://x.com/crypto_expert/status/123456",
    isLoadingPreview: true,
  },
};

export const WithTwitterPreviewMobile: Story = {
  args: {
    ...defaultArgs,
    value: "Check out this post: https://x.com/crypto_expert/status/123456",
    previewData: MOCK_TWITTER_PREVIEW,
  },
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
  },
};

export const WithRedditPreviewMobile: Story = {
  args: {
    ...defaultArgs,
    value: "https://reddit.com/r/security/comments/abc123",
    previewData: MOCK_REDDIT_PREVIEW,
  },
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
  },
};

export const LoadingPreviewMobile: Story = {
  args: {
    ...defaultArgs,
    value: "https://x.com/crypto_expert/status/123456",
    isLoadingPreview: true,
  },
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
  },
};

export const WithPreviewError: Story = {
  args: {
    ...defaultArgs,
    value: "https://x.com/broken_url/status/123",
    previewError: "URL 미리보기를 불러올 수 없습니다.",
  },
};

export const WithPreviewErrorMobile: Story = {
  args: {
    ...defaultArgs,
    value: "https://x.com/broken_url/status/123",
    previewError: "URL 미리보기를 불러올 수 없습니다.",
  },
  parameters: {
    viewport: {
      defaultViewport: "mobile1",
    },
  },
};
