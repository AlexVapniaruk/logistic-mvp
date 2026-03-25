import { apiClient } from './client'
import type { AnalyticsSummary } from './types'

export async function fetchAnalyticsSummary(params: {
  from_ts: string
  to_ts: string
  camera_id?: string
}): Promise<AnalyticsSummary> {
  return apiClient<AnalyticsSummary>('/analytics/summary', { query: params })
}
