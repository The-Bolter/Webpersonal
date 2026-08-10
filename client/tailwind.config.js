/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          light: '#eadcc5',
          DEFAULT: '#e5d5bd',
          dark: '#d9c5a5',
          aged: '#d1bb9a',
          edge: '#c3a682',
        },
        ink: {
          dark: '#3d392d',
          DEFAULT: '#5b5345',
          light: '#8a8072',
          green: '#7a6b55',
          moss: '#8d7d68',
        },
        bark: {
          light: '#b8a48e',
          DEFAULT: '#9a846e',
          dark: '#6b5a48',
        },
        fog: {
          green: 'rgba(122,107,85,0.06)',
          warm: 'rgba(180,164,142,0.05)',
        }
      },
      fontFamily: {
        editorial: ['"Fraunces"', 'Georgia', 'Times New Roman', 'serif'],
        body: ['"Fraunces"', 'Georgia', 'Times New Roman', 'serif'],
        label: ['"Inter"', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        editorial: '0.04em',
        wide: '0.08em',
        label: '0.16em',
      },
      spacing: {
        'section': '10rem',
        'breath': '6rem',
        'whitespace': '12rem',
      },
      borderRadius: {
        'label': '18px',
      },
      transitionDuration: {
        'slow': '800ms',
        'slower': '1200ms',
        'breath': '4000ms',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'breathe': 'breathe 8s ease-in-out infinite',
        'drift': 'drift 12s ease-in-out infinite',
        'fade-in': 'fadeIn 1.6s ease-out forwards',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
        breathe: {
          '0%, 100%': { opacity: '0.92' },
          '50%': { opacity: '1' },
        },
        drift: {
          '0%, 100%': { transform: 'translate(0, 0)' },
          '33%': { transform: 'translate(3px, -2px)' },
          '66%': { transform: 'translate(-2px, 3px)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        inkBleed: {
          '0%': { opacity: '0', filter: 'blur(8px)' },
          '40%': { opacity: '0.5', filter: 'blur(3px)' },
          '100%': { opacity: '1', filter: 'blur(0)' },
        },
      },
    },
  },
  plugins: [],
}
