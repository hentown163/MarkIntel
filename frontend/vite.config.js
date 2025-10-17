import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5000,
    allowedHosts:
      "32522738-9cf2-4737-9dc6-1a4e23e820b8-00-3k6unp11nemit.sisko.replit.dev",
    strictPort: true,
    hmr: {
      clientPort: 443,
      protocol: "wss",
    },
  },
});
