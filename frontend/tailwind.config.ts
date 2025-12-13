import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@aioia/core/dist/**/*.{js,jsx,ts,tsx}",
  ],
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          primary: "#1E9CFD",
          "primary-content": "#FFFFFF",
          secondary: "#88DBFF",
          neutral: "#374151",
          "neutral-content": "#FFFFFF",
          "base-100": "#FFFFFF",
          "base-200": "#F7F7F7",
          "base-300": "#E5E5E5",
          "base-content": "#000000",
          info: "#3ABFF8",
        },
      },
      {
        dark: {
          primary: "#1E9CFD",
          "primary-content": "#FFFFFF",
          secondary: "#88DBFF",
          neutral: "#4B5563",
          "neutral-content": "#FFFFFF",
          "base-100": "#000000",
          "base-200": "#1A1A1A",
          "base-300": "#2D2D2D",
          "base-content": "#FFFFFF",
          info: "#3ABFF8",
        },
      },
    ],
    logs: false,
  },
};

export default config;
