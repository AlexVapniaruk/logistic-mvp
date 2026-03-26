import { defineStore } from 'pinia'
import { fetchEmployees, createEmployee } from '~/api-sdk/employees.api'
import type { Employee, SensorPosition } from '~/api-sdk/types'

interface EmployeesState {
  items: Employee[]
  positions: Record<number, SensorPosition>
  loading: boolean
  error: string | null
}

export const useEmployeesStore = defineStore('employees', {
  state: (): EmployeesState => ({
    items: [],
    positions: {},
    loading: false,
    error: null,
  }),

  actions: {
    async loadEmployees(): Promise<void> {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchEmployees()
      } catch (err) {
        this.error = (err as Error).message
      } finally {
        this.loading = false
      }
    },

    async createEmployee(payload: Omit<Employee, 'id'>): Promise<Employee> {
      this.loading = true
      this.error = null
      try {
        const employee = await createEmployee(payload)
        this.items.push(employee)
        return employee
      } catch (err) {
        this.error = (err as Error).message
        throw err
      } finally {
        this.loading = false
      }
    },

    updatePosition(position: SensorPosition): void {
      this.positions[position.employee_id] = position
    },
  },
})
