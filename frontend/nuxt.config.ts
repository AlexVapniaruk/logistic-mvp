export default defineNuxtConfig({
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss'],

  typescript: {
    strict: true,
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? '/api',
      wsBase: process.env.NUXT_PUBLIC_WS_BASE ?? 'ws://localhost:8000',
    },
  },

  nitro: {
    devProxy: {
      '/api': {
        target: process.env.BACKEND_URL ?? 'http://localhost:8000/api',
        changeOrigin: true,
      },
      '/ws': {
        target: process.env.BACKEND_WS_URL ?? 'ws://localhost:8000/ws',
        ws: true,
      },
    },
  },
})
