/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: { extend: {} },
  plugins: [],
  safelist: [
    'bg-emerald-500',
    'bg-orange-500',
    'bg-sky-500',
    'bg-amber-500',
    'bg-yellow-500'
  ],

}