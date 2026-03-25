import { apiClient } from './client'
import type { ModelVersion, TrainingJob } from './types'

export async function fetchModelVersions(): Promise<ModelVersion[]> {
  return apiClient<ModelVersion[]>('/training/models')
}

export async function startTraining(config: Record<string, unknown>): Promise<TrainingJob> {
  return apiClient<TrainingJob>('/training/start', { method: 'POST', body: config })
}

export async function fetchTrainingStatus(jobId: number): Promise<TrainingJob> {
  return apiClient<TrainingJob>(`/training/jobs/${jobId}`)
}
