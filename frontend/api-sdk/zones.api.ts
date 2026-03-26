import { apiClient } from './client'
import type { Zone } from './types'

export async function fetchZones(terminalId: number): Promise<Zone[]> {
  return apiClient<Zone[]>(`/terminals/${terminalId}/zones/`)
}

export async function createZone(
  terminalId: number,
  payload: Pick<Zone, 'name' | 'points'>
): Promise<Zone> {
  return apiClient<Zone>(`/terminals/${terminalId}/zones/`, { method: 'POST', body: payload })
}
