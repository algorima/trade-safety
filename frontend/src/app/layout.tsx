import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Trade Safety - K-pop Merchandise Trade Safety Check",
  description:
    "AI-powered safety analysis for K-pop merchandise trading. Detect scams, understand Korean slang, and make safer trades.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
