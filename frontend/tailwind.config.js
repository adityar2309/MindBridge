/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'mood-happy': '#10b981',
        'mood-neutral': '#6b7280',
        'mood-sad': '#9ca3af',
        'mood-stressed': '#ef4444',
        'mood-calm': '#3b82f6',
      }
    },
  },
  plugins: [],
} 