import { apiClient } from './client'
import type { Camera } from './types'

export async function fetchCameras(): Promise<Camera[]> {
  return apiClient<Camera[]>('/cameras/')
}

export async function createCamera(payload: Omit<Camera, 'id'>): Promise<Camera> {
  return apiClient<Camera>('/cameras/', { method: 'POST', body: payload })
}

export async function updateCamera(
  id: number,
  payload: Partial<Omit<Camera, 'id' | 'terminal_id'>>
): Promise<Camera> {
  return apiClient<Camera>(`/cameras/${id}`, { method: 'PATCH', body: payload })
}
