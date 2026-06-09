/** @type {import('tailwindcss').Config}*/
const config = {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
  ],

  plugins: [require("flowbite/plugin")],

  darkMode: "class",

  theme: {
    fontFamily: {
      display: ['Roboto', ''],
      body: ['Roboto', ''],
    },
    extend: {
      colors: {
        // flowbite-svelte — matched to HCIstudio teal logo
        primary: {
          50:  '#edfafa',
          100: '#d5f5f5',
          200: '#aaeaea',
          300: '#72d9d9',
          400: '#3dc4c4',
          500: '#1aadad',
          600: '#0f9090',
          700: '#0d7373',
          800: '#0a5a5a',
          900: '#083d3d',
        }
      },
    },
  },
};

module.exports = config;
