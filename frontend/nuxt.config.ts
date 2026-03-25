export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],

  css: ['~/assets/scss/main.scss'],

  typescript: {
    strict: true,
  },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          // Makes abstracts (variables + mixins) available in every SFC <style>
          additionalData: '@use "~/assets/scss/abstracts" as *;',
        },
      },
    },
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
