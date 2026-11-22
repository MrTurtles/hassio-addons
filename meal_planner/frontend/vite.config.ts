import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vitest/config";

function ingressBase(): Plugin {
  return {
    name: "ingress-base",
    transformIndexHtml: {
      order: "pre",
      handler(html, ctx) {
        if (!ctx.server) {
          return html;
        }
        return html.replaceAll("__INGRESS_BASE_HREF__", "/");
      },
    },
  };
}

export default defineConfig({
  plugins: [react(), tailwindcss(), ingressBase()],
  base: "./",
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        headers: { "X-MealPlanner-Channel": "development" },
      },
    },
  },
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
});
