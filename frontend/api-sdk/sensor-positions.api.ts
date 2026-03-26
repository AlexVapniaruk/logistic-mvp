import { apiClient } from './client'
import type { SensorPosition } from './types'

export async function createSensorPosition(
  payload: Pick<SensorPosition, 'employee_id' | 'x' | 'y' | 'timestamp'>
): Promise<SensorPosition> {
  return apiClient<SensorPosition>('/sensor-positions/', { method: 'POST', body: payload })
}
