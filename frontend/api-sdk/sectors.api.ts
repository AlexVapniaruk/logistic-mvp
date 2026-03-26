import { apiClient } from './client'
import type { Sector } from './types'

export async function fetchSectors(zoneId: number): Promise<Sector[]> {
  return apiClient<Sector[]>(`/zones/${zoneId}/sectors/`)
}

export async function createSector(
  zoneId: number,
  payload: Pick<Sector, 'name' | 'points'>
): Promise<Sector> {
  return apiClient<Sector>(`/zones/${zoneId}/sectors/`, { method: 'POST', body: payload })
}
