import { apiClient } from './client'
import type { Annotation } from './types'

export async function createAnnotation(
  payload: Pick<Annotation, 'camera_event_id' | 'annotator_id' | 'action_type' | 'notes'>
): Promise<Annotation> {
  return apiClient<Annotation>('/annotations/', { method: 'POST', body: payload })
}
