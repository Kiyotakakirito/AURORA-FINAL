/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Aurora Theme - Deep Teal & Cyan
        aurora: {
          900: '#001a1a',
          800: '#002d2d',
          700: '#004040',
          600: '#005454',
          500: '#006b6b',
          400: '#008080',
          300: '#00a0a0',
          200: '#00d4d4',
          100: '#00f0f0',
          50: '#e6ffff',
        },
        // Primary Glow Colors
        glow: {
          cyan: '#00f0ff',
          teal: '#00d4aa',
          green: '#00ff9d',
        },
        // Dark backgrounds
        deep: {
          1000: '#000a0f',
          900: '#001219',
          800: '#001a23',
          700: '#002028',
        },
        // Accent colors for features
        feature: {
          1: '#00d4ff', // Cyan for Feature 1
          2: '#00ff9d', // Green for Feature 2
          3: '#a855f7', // Purple for Feature 3
          4: '#f97316', // Orange for Feature 4
          5: '#00d4aa', // Teal for Feature 5
        }
      },
      backgroundImage: {
        'aurora-gradient': 'linear-gradient(135deg, #001a1a 0%, #002d2d 50%, #001219 100%)',
        'glow-gradient': 'linear-gradient(135deg, #00d4aa 0%, #00f0ff 50%, #00ff9d 100%)',
        'card-gradient': 'linear-gradient(145deg, rgba(0,45,45,0.9) 0%, rgba(0,26,26,0.95) 100%)',
      },
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(0, 240, 255, 0.3)',
        'glow-teal': '0 0 20px rgba(0, 212, 170, 0.3)',
        'glow-strong': '0 0 30px rgba(0, 240, 255, 0.5)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00d4aa, 0 0 10px #00d4aa' },
          '100%': { boxShadow: '0 0 20px #00f0ff, 0 0 30px #00f0ff' },
        },
      },
    },
  },
  plugins: [],
}
