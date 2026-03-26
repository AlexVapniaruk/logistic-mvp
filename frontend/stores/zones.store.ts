import { defineStore } from 'pinia'
import { fetchZones, createZone } from '~/api-sdk/zones.api'
import type { Zone } from '~/api-sdk/types'

interface ZonesState {
  items: Zone[]
  loading: boolean
  error: string | null
}

export const useZonesStore = defineStore('zones', {
  state: (): ZonesState => ({
    items: [],
    loading: false,
    error: null,
  }),

  actions: {
    async loadZones(terminalId: number): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchZones(terminalId)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async createZone(terminalId: number, payload: Pick<Zone, 'name' | 'points'>): Promise<Zone> {
      this.loading = true
      this.error = null
      try {
        const zone = await createZone(terminalId, payload)
        this.items.push(zone)
        return zone
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
