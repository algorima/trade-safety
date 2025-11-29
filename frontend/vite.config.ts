import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import dts from "vite-plugin-dts";
import pkg from "./package.json" with { type: "json" };

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, "src/index.ts"),
      formats: ["es", "cjs"],
      fileName: (format) => `index.${format === "es" ? "js" : "cjs"}`,
    },
    rollupOptions: {
      external: [
        // Automatically externalize peerDependencies
        ...Object.keys(pkg.peerDependencies || {}),
        // Automatically externalize dependencies (install but don't bundle)
        ...Object.keys(pkg.dependencies || {}).filter(
          // Bundle small utilities, externalize others
          (dep) => !["clsx"].includes(dep),
        ),
        // Add peer submodules explicitly
        "react/jsx-runtime",
        /^next\//,
      ],
    },
  },
  plugins: [
    react(),
    dts({
      include: [
        "src/components/**/*",
        "src/repositories/**/*",
        "src/types.ts",
        "src/index.ts",
      ],
      exclude: [
        "src/app",
        "**/*.test.ts",
        "**/*.test.tsx",
        "**/*.stories.ts",
        "**/*.stories.tsx",
      ],
    }),
  ],
});
