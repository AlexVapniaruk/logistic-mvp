import { apiClient } from './client'
import type { Employee } from './types'

export async function fetchEmployees(): Promise<Employee[]> {
  return apiClient<Employee[]>('/employees/')
}

export async function createEmployee(payload: Omit<Employee, 'id'>): Promise<Employee> {
  return apiClient<Employee>('/employees/', { method: 'POST', body: payload })
}
