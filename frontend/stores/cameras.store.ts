import { defineStore } from 'pinia'
import { fetchCameras, createCamera, updateCamera } from '~/api-sdk/cameras.api'
import type { Camera } from '~/api-sdk/types'

interface CamerasState {
  items: Camera[]
  loading: boolean
  error: string | null
}

export const useCamerasStore = defineStore('cameras', {
  state: (): CamerasState => ({
    items: [],
    loading: false,
    error: null,
  }),

  actions: {
    async loadCameras(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchCameras()
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async createCamera(payload: Omit<Camera, 'id'>): Promise<Camera> {
      this.loading = true
      this.error = null
      try {
        const camera = await createCamera(payload)
        this.items.push(camera)
        return camera
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateCamera(id: number, payload: Partial<Omit<Camera, 'id' | 'terminal_id'>>): Promise<void> {
      this.loading = true
      this.error = null
      try {
        const updated = await updateCamera(id, payload)
        const idx = this.items.findIndex(c => c.id === id)
        if (idx !== -1) this.items[idx] = updated
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
