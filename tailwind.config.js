import tailwind_forms from '@tailwindcss/forms'
import daisyui from "daisyui"

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/templates/**/*.html',
    './src/**/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    tailwind_forms,
    daisyui
  ],
  daisyui: {
    themes: [
      'sunset'
    ]
  }
}