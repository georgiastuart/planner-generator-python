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
        'gn-landscape': '16 / 10'
      },
      width: {
        'gn-landscape': '18.83in'
      },
      height: {
        'gn-landscape': '11.77in',
        '5mm': '10.4167mm',
        '10mm': '20.84mm',
        '15mm': '31.25mm',
        '20mm': '41.6667mm',
        '25mm': '52.08mm'
      }
    },
  },
  plugins: [],
}
