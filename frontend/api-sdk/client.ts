import { $fetch } from 'ofetch'

const getBaseUrl = (): string => {
  if (typeof window !== 'undefined') {
    return (window as Window & { __NUXT__?: { config?: { public?: { apiBase?: string } } } })
      ?.__NUXT__?.config?.public?.apiBase ?? '/api'
  }
  return process.env.NUXT_PUBLIC_API_BASE ?? 'http://backend:8000/api'
}

export const apiClient = $fetch.create({
  get baseURL() {
    return getBaseUrl()
  },
  headers: {
    'Content-Type': 'application/json',
  },
})
