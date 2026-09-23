/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Core navy/slate foundation — deliberately cool and quiet so the
        // teal/blue accent pair (see below) is the only saturated color.
        base: {
          950: '#080B11',
          900: '#0B0F17',
          800: '#121826',
          700: '#1A2332',
          600: '#232E3F',
          500: '#3A465A',
          400: '#5B677C',
        },
        ink: {
          100: '#EDF1F7',
          200: '#C7D0DE',
          300: '#8D98AC',
          400: '#6B7688',
        },
        // Single accent family, two temperatures of the same hue pair —
        // signal (blue) for actions/links, current (teal) for AI/live states.
        signal: {
          400: '#5C8DFF',
          500: '#3E6EFA',
          600: '#2E54D9',
        },
        current: {
          400: '#3FE8C7',
          500: '#21D4B4',
          600: '#16A88F',
        },
        amber: {
          400: '#F0A857',
          500: '#E0912E',
        },
      },
      fontFamily: {
        sans: ['"Geist Sans"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"Geist Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      maxWidth: {
        shell: '1440px',
      },
      boxShadow: {
        diffuse: '0 30px 80px -30px rgba(0,0,0,0.55)',
        'ring-current': '0 0 0 1px rgba(33,212,180,0.35)',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: 0, transform: 'translateY(10px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        'pulse-dot': {
          '0%, 80%, 100%': { transform: 'scale(0.6)', opacity: 0.35 },
          '40%': { transform: 'scale(1)', opacity: 1 },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'fade-up': 'fade-up 500ms cubic-bezier(0.23,1,0.32,1) both',
        'pulse-dot': 'pulse-dot 1.1s ease-in-out infinite',
        shimmer: 'shimmer 2.2s linear infinite',
      },
      transitionTimingFunction: {
        out: 'cubic-bezier(0.23, 1, 0.32, 1)',
        inout: 'cubic-bezier(0.77, 0, 0.175, 1)',
      },
    },
  },
  plugins: [],
};
