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

export type WsMessageType = 'event' | 'inference_result' | 'training_progress' | 'error' | 'position_update'

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

// --- Worker tracking ---

export interface Terminal {
  id: number
  name: string
  description: string | null
  map_image_url: string | null
}

export interface Zone {
  id: number
  name: string
  points: [number, number][]
  terminal_id: number
}

export interface Sector {
  id: number
  name: string
  points: [number, number][]
  zone_id: number
}

export interface Camera {
  id: number
  name: string
  stream_url: string
  terminal_id: number
  zone_id: number | null
  sector_id: number | null
}

export interface Employee {
  id: number
  name: string
  badge_id: string
  terminal_id: number
}

export interface SensorPosition {
  id: number
  employee_id: number
  x: number
  y: number
  zone_id: number | null
  sector_id: number | null
  timestamp: string
}

export interface CameraEvent {
  id: number
  camera_id: number
  timestamp: string
  action_type: string
  confidence: number
  bounding_box: number[] | null
  video_clip_url: string | null
  needs_annotation: boolean
  employee_action_id: number | null
}

export interface EmployeeAction {
  id: number
  employee_id: number
  zone_id: number
  sector_id: number | null
  action_type: string
  confidence: number
  source_event_id: number | null
  timestamp: string
}

export interface Annotation {
  id: number
  camera_event_id: number
  annotator_id: string
  action_type: string
  notes: string | null
  created_at: string
}

export interface HeatmapEntry {
  zone_id: number
  zone_name: string
  count: number
  sector_breakdown: Record<string, number>
}

export interface HeatmapResponse {
  entries: HeatmapEntry[]
  from_ts: string | null
  to_ts: string | null
}

export interface ZoneAnalytics {
  zone_id: number
  zone_name: string
  action_count: number
}

export interface EmployeeAnalytics {
  employee_id: number
  action_counts: Record<string, number>
  total: number
}
