<script setup lang="ts">
import type { SensorPosition } from '~/api-sdk/types'

const props = defineProps<{
  positions: Record<number, SensorPosition>
  mapWidth: number
  mapHeight: number
}>()
</script>

<template>
  <svg
    class="position-overlay"
    :viewBox="`0 0 ${mapWidth} ${mapHeight}`"
    preserveAspectRatio="xMidYMid meet"
  >
    <circle
      v-for="(pos, employeeId) in positions"
      :key="employeeId"
      :cx="pos.x"
      :cy="pos.y"
      r="8"
      class="position-overlay__dot"
    >
      <title>Employee {{ employeeId }}</title>
    </circle>
  </svg>
</template>

<style lang="scss" scoped>
.position-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;

  @include element(dot) {
    fill: $color-primary;
    opacity: 0.85;
    transition: opacity $transition-fast;

    @include modifier(active) {
      fill: $color-success;
    }
  }
}
</style>
