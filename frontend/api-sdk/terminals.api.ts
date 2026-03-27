import { $fetch } from 'ofetch'
import { apiClient, getBaseUrl } from './client'
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

export async function updateTerminal(
  id: number,
  payload: Partial<Omit<Terminal, 'id'>>
): Promise<Terminal> {
  return apiClient<Terminal>(`/terminals/${id}`, { method: 'PATCH', body: payload })
}

export async function uploadTerminalImage(id: number, file: File): Promise<Terminal> {
  const form = new FormData()
  form.append('file', file)
  return $fetch<Terminal>(`${getBaseUrl()}/terminals/${id}/upload-image`, {
    method: 'POST',
    body: form,
  })
}
