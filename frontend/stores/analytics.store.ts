import { defineStore } from 'pinia'
import { fetchAnalyticsSummary } from '~/api-sdk/analytics.api'
import type { AnalyticsSummary } from '~/api-sdk/types'

interface AnalyticsState {
  summary: AnalyticsSummary | null
  loading: boolean
  error: string | null
}

export const useAnalyticsStore = defineStore('analytics', {
  state: (): AnalyticsState => ({
    summary: null,
    loading: false,
    error: null,
  }),

  actions: {
    async loadSummary(params: { from_ts: string; to_ts: string; camera_id?: string }): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.summary = await fetchAnalyticsSummary(params)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },
  },
})
