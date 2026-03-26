import { apiClient } from './client'
import type { Terminal } from './types'

export async function fetchTerminals(): Promise<Terminal[]> {
  return apiClient<Terminal[]>('/terminals/')
}

export async function fetchTerminal(id: number): Promise<Terminal> {
  return apiClient<Terminal>(`/terminals/${id}`)
}

export async function createTerminal(payload: Omit<Terminal, 'id'>): Promise<Terminal> {
  return apiClient<Terminal>('/terminals/', { method: 'POST', body: payload })
}
