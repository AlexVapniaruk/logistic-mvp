<script setup lang="ts">
import type { Employee, SensorPosition } from '~/api-sdk/types'

defineProps<{
  employee: Employee
  position: SensorPosition | null
}>()
</script>

<template>
  <div class="employee-card card">
    <div class="card__header">
      <span class="employee-card__name">{{ employee.name }}</span>
      <span class="badge badge--info">{{ employee.badge_id }}</span>
    </div>
    <div class="card__body">
      <div v-if="position" class="employee-card__position">
        <span class="employee-card__coord">x: {{ position.x.toFixed(1) }}</span>
        <span class="employee-card__coord">y: {{ position.y.toFixed(1) }}</span>
        <span v-if="position.zone_id" class="badge badge--success">Zone {{ position.zone_id }}</span>
        <span v-else class="badge badge--warning">No zone</span>
      </div>
      <div v-else class="employee-card__no-position">No position data</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.employee-card {
  @include element(name) {
    font-weight: $font-weight-medium;
  }

  @include element(position) {
    @include flex(row, center, flex-start, $spacing-2);
    flex-wrap: wrap;
  }

  @include element(coord) {
    font-family: $font-family-mono;
    font-size: $font-size-sm;
  }

  @include element(no-position) {
    font-size: $font-size-sm;
    opacity: 0.5;
  }
}
</style>
