// Mirrors backend Pydantic schemas exactly.
// This is the single source of truth for API shapes on the frontend.

export interface ActionClass {
  id: number
  name: string
  label: string
  confidence_threshold: number
}

export interface Event {
  id: number
  camera_id: string
  action_class: string
  confidence: number
  timestamp: string
  frame_path: string | null
  metadata: Record<string, unknown>
}

export interface EventFilter {
  camera_id?: string
  action_class?: string
  from_ts?: string
  to_ts?: string
  limit?: number
  offset?: number
}

export interface ModelVersion {
  id: number
  name: string
  path: string
  is_active: boolean
  created_at: string
  metrics: Record<string, number>
}

export interface TrainingJob {
  id: number
  status: TrainingStatus
  model_version_id: number | null
  started_at: string
  finished_at: string | null
  config: Record<string, unknown>
  error: string | null
}

export type TrainingStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface AnalyticsSummary {
  total_events: number
  events_by_class: Record<string, number>
  events_by_camera: Record<string, number>
  avg_confidence: number
  period_start: string
  period_end: string
}

export interface WsMessage {
  type: WsMessageType
  payload: unknown
}

export type WsMessageType = 'event' | 'inference_result' | 'training_progress' | 'error'

export interface InferenceResult {
  camera_id: string
  detections: Detection[]
  frame_id: number
  timestamp: string
}

export interface Detection {
  class_name: string
  confidence: number
  bbox: [number, number, number, number]
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}
