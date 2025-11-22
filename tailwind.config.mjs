/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				background: '#09090b', // Zinc 950
				surface: '#18181b',    // Zinc 900
				'surface-hover': '#27272a', // Zinc 800
				border: '#27272a',     // Zinc 800
				primary: '#fafafa',    // Zinc 50
				secondary: '#a1a1aa',  // Zinc 400
				accent: '#f4f4f5',     // Zinc 100
			},
			fontFamily: {
				sans: ['Inter', 'sans-serif'],
				mono: ['JetBrains Mono', 'monospace'],
				serif: ['Playfair Display', 'serif'],
				hand: ['Patrick Hand', 'cursive'],
			},
			animation: {
				'fade-in': 'fadeIn 0.5s ease-out forwards',
				'slide-up': 'slideUp 0.5s ease-out forwards',
			},
			keyframes: {
				fadeIn: {
					'0%': { opacity: '0' },
					'100%': { opacity: '1' },
				},
				slideUp: {
					'0%': { opacity: '0', transform: 'translateY(10px)' },
					'100%': { opacity: '1', transform: 'translateY(0)' },
				},
			},
		},
	},
	plugins: [],
}