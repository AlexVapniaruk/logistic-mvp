import { defineStore } from 'pinia'
import { createAnnotation } from '~/api-sdk/annotations.api'
import type { Annotation } from '~/api-sdk/types'
import { useCameraEventsStore } from '~/stores/camera-events.store'

interface AnnotationsState {
  lastCreated: Annotation | null
  loading: boolean
  error: string | null
}

export const useAnnotationsStore = defineStore('annotations', {
  state: (): AnnotationsState => ({
    lastCreated: null,
    loading: false,
    error: null,
  }),

  actions: {
    async submitAnnotation(
      payload: Pick<Annotation, 'camera_event_id' | 'annotator_id' | 'action_type' | 'notes'>
    ): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.lastCreated = await createAnnotation(payload)
        await useCameraEventsStore().loadAnnotationQueue()
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
