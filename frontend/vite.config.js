import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

const sourceRoot = fileURLToPath(new URL('./src', import.meta.url))
const projectRoot = fileURLToPath(new URL('.', import.meta.url))
const outputRoot = fileURLToPath(new URL('./dist', import.meta.url))

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, projectRoot, '')
  const dataMode = env.VITE_DATA_MODE || (mode === 'api' ? 'api' : 'mock')
  const usesDeploymentBase = command === 'build' || mode === 'production'
  const base = usesDeploymentBase ? (env.VITE_BASE_PATH || '/amazon-tk-agents/') : '/'

  return {
    base,
    define: {
      'import.meta.env.VITE_DATA_MODE': JSON.stringify(dataMode),
    },
    root: sourceRoot,
    plugins: [vue()],
    resolve: {
      alias: {
        '@': sourceRoot,
      },
    },
    server: {
      fs: {
        allow: [projectRoot],
      },
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8081',
          changeOrigin: true,
        },
      },
    },
    build: {
      outDir: outputRoot,
      emptyOutDir: true,
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
  }
})
