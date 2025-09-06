/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.html',             // ✅ this is important
    './**/*.js',
    './**/*.py',               // optional for class names in views
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}