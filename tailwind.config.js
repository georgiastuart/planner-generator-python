/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,j2}"],
  theme: {
    extend: {
      fontFamily: {
        'playfair': ['Playfair Display', 'serif']
      },
      aspectRatio: {
        'gn-portrait': '1 / 1.29',
        'gn-landscape': '16 / 10',
        'gn-slim': '1 / 2.36'
      },
      width: {
        'gn-landscape': '18.83in',
        'gn-slim': '5.0in'
      },
      height: {
        'gn-landscape': '11.5in',
        'gn-slim': '11.5in',
        '5mm': '10.4167mm',
        '10mm': '20.84mm',
        '15mm': '31.25mm',
        '20mm': '41.6667mm',
        '25mm': '52.08mm'
      },
      spacing: {
        '5mm': '10.4167mm'
      },
      colors: {
        'dark': '#333333'
      },
      gridTemplateColumns: {
        '13': 'repeat(13, minmax(0, 1fr))',
      }
    },
  },
  plugins: [],
}
