import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        base: "#0A1420",
        surface: "#101B2D",
        "surface-raised": "#152239",
        border: "#22314A",
        ink: "#E8EEF7",
        muted: "#8CA0BF",
        accent: {
          teal: "#4FD1C5",
          blue: "#5B8DEF",
        },
        status: {
          good: "#4ADE80",
          warn: "#F5B461",
          bad: "#F2726A",
        },
      },
      fontFamily: {
        display: ["var(--font-space-grotesk)", "system-ui", "sans-serif"],
        body: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "10px",
      },
    },
  },
  plugins: [],
};

export default config;
