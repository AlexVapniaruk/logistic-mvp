import { defineStore } from 'pinia'
import { fetchEvents, fetchEvent } from '~/api-sdk/events.api'
import type { Event, EventFilter, PaginatedResponse } from '~/api-sdk/types'

interface EventsState {
  items: Event[]
  total: number
  selected: Event | null
  loading: boolean
  error: string | null
}

export const useEventsStore = defineStore('events', {
  state: (): EventsState => ({
    items: [],
    total: 0,
    selected: null,
    loading: false,
    error: null,
  }),

  actions: {
    async loadEvents(filters: EventFilter = {}): Promise<void> {
      this.loading = true
      this.error = null
      try {
        const result: PaginatedResponse<Event> = await fetchEvents(filters)
        this.items = result.items
        this.total = result.total
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async loadEvent(id: number): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.selected = await fetchEvent(id)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    pushEvent(event: Event): void {
      this.items.unshift(event)
      this.total++
    },
  },
})
