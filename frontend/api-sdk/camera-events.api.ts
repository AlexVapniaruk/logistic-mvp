import { apiClient } from './client'
import type { CameraEvent } from './types'

export interface CameraEventFilters {
  needs_annotation?: boolean
  camera_id?: number
  limit?: number
  offset?: number
}

export async function fetchCameraEvents(filters: CameraEventFilters = {}): Promise<CameraEvent[]> {
  return apiClient<CameraEvent[]>('/camera-events/', { query: filters })
}

export async function createCameraEvent(
  payload: Pick<CameraEvent, 'camera_id' | 'timestamp' | 'action_type' | 'confidence' | 'bounding_box' | 'video_clip_url'>
): Promise<CameraEvent> {
  return apiClient<CameraEvent>('/camera-events/', { method: 'POST', body: payload })
}
