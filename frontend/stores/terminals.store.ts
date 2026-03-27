import { defineStore } from 'pinia'
import { fetchTerminals, fetchTerminal, createTerminal, updateTerminal, uploadTerminalImage } from '~/api-sdk/terminals.api'
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
    selectTerminal(terminal: Terminal): void {
      this.selected = terminal
      if (import.meta.client) {
        localStorage.setItem('selectedTerminalId', String(terminal.id))
      }
    },

    clearTerminal(): void {
      this.selected = null
      if (import.meta.client) {
        localStorage.removeItem('selectedTerminalId')
      }
    },

    async loadTerminals(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchTerminals()
        // Restore saved selection on first load
        if (!this.selected && import.meta.client) {
          const savedId = localStorage.getItem('selectedTerminalId')
          if (savedId) {
            const found = this.items.find(t => t.id === Number(savedId))
            if (found) this.selected = found
          }
        }
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

    async updateTerminal(id: number, payload: Partial<Omit<Terminal, 'id'>>): Promise<void> {
      this.error = null
      try {
        const updated = await updateTerminal(id, payload)
        if (this.selected?.id === id) this.selected = updated
        const idx = this.items.findIndex(t => t.id === id)
        if (idx !== -1) this.items[idx] = updated
      } catch (err) {
        this.error = (err as Error).message
        throw err
      }
    },

    async uploadImage(id: number, file: File): Promise<void> {
      this.error = null
      try {
        const updated = await uploadTerminalImage(id, file)
        if (this.selected?.id === id) this.selected = updated
        const idx = this.items.findIndex(t => t.id === id)
        if (idx !== -1) this.items[idx] = updated
      } catch (err) {
        this.error = (err as Error).message
        throw err
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
