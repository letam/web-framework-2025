import path from 'path'
import { VitePWA } from 'vite-plugin-pwa'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const NODE_ENV = process.env.NODE_ENV ?? '';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), VitePWA({
    strategies: 'injectManifest',
    srcDir: 'src',
    filename: 'sw.ts',
    registerType: 'prompt',
    injectRegister: false,

    pwaAssets: {
      disabled: false,
      config: true,
    },

    manifest: {
      name: 'app',
      short_name: 'app',
      description: 'app',
      theme_color: '#ffffff',
    },

    injectManifest: {
      globPatterns: ['**/*.{js,css,html,svg,png,ico}'],
    },

    devOptions: {
      enabled: false,
      navigateFallback: 'index.html',
      suppressWarnings: true,
      type: 'module',
    },
  })],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  ...(NODE_ENV === 'development' ? {
  } : {
    // Reference: https://vite.dev/config/shared-options.html#base ; https://vite.dev/guide/build.html#public-base-path
    base: '/static/app/',
  }),
})