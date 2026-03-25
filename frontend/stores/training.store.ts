import { defineStore } from 'pinia'
import { fetchModelVersions, startTraining, fetchTrainingStatus } from '~/api-sdk/training.api'
import type { ModelVersion, TrainingJob } from '~/api-sdk/types'

interface TrainingState {
  models: ModelVersion[]
  activeJob: TrainingJob | null
  loading: boolean
  error: string | null
}

export const useTrainingStore = defineStore('training', {
  state: (): TrainingState => ({
    models: [],
    activeJob: null,
    loading: false,
    error: null,
  }),

  getters: {
    activeModel: (state): ModelVersion | undefined =>
      state.models.find((m) => m.is_active),
  },

  actions: {
    async loadModels(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.models = await fetchModelVersions()
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async startJob(config: Record<string, unknown>): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.activeJob = await startTraining(config)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async pollJobStatus(jobId: number): Promise<void> {
      try {
        this.activeJob = await fetchTrainingStatus(jobId)
      } catch (err) {
        this.error = (err as Error).message
      }
    },
  },
})
