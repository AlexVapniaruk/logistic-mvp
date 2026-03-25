import { apiClient } from './client'
import type { Event, EventFilter, PaginatedResponse } from './types'

export async function fetchEvents(filters: EventFilter = {}): Promise<PaginatedResponse<Event>> {
  return apiClient<PaginatedResponse<Event>>('/events', { query: filters })
}

export async function fetchEvent(id: number): Promise<Event> {
  return apiClient<Event>(`/events/${id}`)
}

export async function createEvent(payload: Omit<Event, 'id'>): Promise<Event> {
  return apiClient<Event>('/events', { method: 'POST', body: payload })
}
