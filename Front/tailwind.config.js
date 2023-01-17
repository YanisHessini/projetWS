/** @type {import('tailwindcss').Config} */

module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{html,vue,js,ts,jsx,tsx,svelte,md}'],
  theme: {
    extend: {
      fontFamily: {
        //@ts-ignore
        sans: [
          'Inter var',
          ...require('tailwindcss/defaultTheme').fontFamily.sans,
        ],
      },
    },
  },
	plugins: [
		require('@tailwindcss/forms'),
		require("daisyui")
	],
	daisyui: {
		themes: false,
	},
}
