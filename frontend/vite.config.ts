import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import dts from "vite-plugin-dts";
import pkg from "./package.json";

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  build: {
    sourcemap: true,
    lib: {
      entry: {
        index: resolve(__dirname, "src/index.ts"),
        locale: resolve(__dirname, "src/i18n/translations.ts"),
      },
      formats: ["es", "cjs"],
      fileName: (format, entryName) =>
        `${entryName}.${format === "es" ? "mjs" : "js"}`,
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
        "src/i18n/translations.ts",
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
