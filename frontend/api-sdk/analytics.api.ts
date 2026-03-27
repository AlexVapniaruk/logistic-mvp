import { apiClient } from './client'
import type { AnalyticsSummary, ZoneLiveResponse } from './types'

export async function fetchAnalyticsSummary(params: {
  from_ts: string
  to_ts: string
  camera_id?: string
}): Promise<AnalyticsSummary> {
  return apiClient<AnalyticsSummary>('/analytics/summary', { query: params })
}

export async function fetchLiveZoneStats(windowMinutes = 5, terminalId?: number): Promise<ZoneLiveResponse> {
  return apiClient<ZoneLiveResponse>('/analytics/zones/live', {
    query: { window_minutes: windowMinutes, ...(terminalId !== undefined && { terminal_id: terminalId }) },
  })
}
