import { defineStore } from 'pinia'
import { fetchSectors, createSector } from '~/api-sdk/sectors.api'
import type { Sector } from '~/api-sdk/types'

interface SectorsState {
  items: Sector[]
  loading: boolean
  error: string | null
}

export const useSectorsStore = defineStore('sectors', {
  state: (): SectorsState => ({
    items: [],
    loading: false,
    error: null,
  }),

  actions: {
    async loadSectors(zoneId: number): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchSectors(zoneId)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async createSector(zoneId: number, payload: Pick<Sector, 'name' | 'points'>): Promise<Sector> {
      this.loading = true
      this.error = null
      try {
        const sector = await createSector(zoneId, payload)
        this.items.push(sector)
        return sector
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
