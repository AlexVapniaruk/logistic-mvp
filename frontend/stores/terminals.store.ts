import { defineStore } from 'pinia'
import { fetchTerminals, fetchTerminal, createTerminal } from '~/api-sdk/terminals.api'
import type { Terminal } from '~/api-sdk/types'

interface TerminalsState {
  items: Terminal[]
  selected: Terminal | null
  loading: boolean
  error: string | null
}

export const useTerminalsStore = defineStore('terminals', {
  state: (): TerminalsState => ({
    items: [],
    selected: null,
    loading: false,
    error: null,
  }),

  actions: {
    async loadTerminals(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchTerminals()
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async loadTerminal(id: number): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.selected = await fetchTerminal(id)
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async createTerminal(payload: Omit<Terminal, 'id'>): Promise<Terminal> {
      this.loading = true
      this.error = null
      try {
        const terminal = await createTerminal(payload)
        this.items.push(terminal)
        return terminal
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
