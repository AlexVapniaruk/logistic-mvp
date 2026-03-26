import { defineStore } from 'pinia'
import { fetchCameraEvents } from '~/api-sdk/camera-events.api'
import type { CameraEvent } from '~/api-sdk/types'

interface CameraEventsState {
  items: CameraEvent[]
  annotationQueue: CameraEvent[]
  loading: boolean
  error: string | null
}

export const useCameraEventsStore = defineStore('camera-events', {
  state: (): CameraEventsState => ({
    items: [],
    annotationQueue: [],
    loading: false,
    error: null,
  }),

  actions: {
    async loadCameraEvents(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchCameraEvents()
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async loadAnnotationQueue(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.annotationQueue = await fetchCameraEvents({ needs_annotation: true })
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },
  },
})
