import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    origin: 'http://localhost:5173',
    cors: 'http://localhost:8080',
  },
  root: resolve("./src"),
  base: "/static/dist/",
  build: {
    manifest: 'manifest.json',
    emptyOutDir: true,
    outDir: resolve("./dist"),
    rollupOptions: {
      input: {
        resources_app: resolve('./src/resources_app.js'),
        backdrop_media_app: resolve('./src/backdrop_media_app.js'),
        shikwasa_player_app: resolve('./src/shikwasa_player_app.js'),
        aplayer_app: resolve('./src/aplayer_app.js'),
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: 'legacy'
      },
      sass: {
        api: 'legacy'
      },
    }
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
