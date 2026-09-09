import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

const sourceRoot = fileURLToPath(new URL('./src', import.meta.url))
const outputRoot = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  root: sourceRoot,
  plugins: [vue()],
  resolve: {
    alias: {
      '@': sourceRoot,
    },
  },
  server: {
    fs: {
      allow: [outputRoot],
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8081',
        changeOrigin: true,
      },
    },
  },
  build: {
    // FastAPI 挂载 output/，因此构建产物直接落在 output 根目录。
    outDir: outputRoot,
    emptyOutDir: false,
    assetsDir: 'assets',
    rollupOptions: {
      input: fileURLToPath(new URL('./src/index.html', import.meta.url)),
      output: {
        manualChunks: {
          'ui-vendor': ['vue', 'vue-router', 'ant-design-vue', '@ant-design/icons-vue'],
          'chart-vendor': ['echarts'],
          'http-vendor': ['axios'],
        },
      },
    },
    chunkSizeWarningLimit: 900,
  },
})
