<script setup lang="ts">
import { onMounted } from 'vue'
import { useEventsStore } from '~/stores/events.store'
import { useEmployeesStore } from '~/stores/employees.store'
import { useWebSocket } from '~/composables/useWebSocket'
import type { WsMessage, Event, SensorPosition } from '~/api-sdk/types'

const store = useEventsStore()
const employeesStore = useEmployeesStore()
const { on } = useWebSocket('/ws/live')
const { on: onPosition } = useWebSocket('/ws/positions')

onMounted(() => {
  store.loadEvents({ limit: 50 })
  employeesStore.loadEmployees()
  on('event', (msg: WsMessage) => store.pushEvent(msg.payload as Event))
  onPosition('position_update', (msg: WsMessage) =>
    employeesStore.updatePosition(msg.payload as SensorPosition)
  )
})
</script>

<template>
  <div class="live-dashboard">
    <h1 class="live-dashboard__title">Live Dashboard</h1>

    <div class="live-dashboard__layout">
      <section class="live-dashboard__map-section">
        <EmployeePositionOverlay
          :positions="employeesStore.positions"
          :map-width="800"
          :map-height="600"
        />
      </section>

      <section class="live-dashboard__events">
        <div v-if="store.loading" class="live-dashboard__state">Connecting…</div>
        <div v-else-if="store.error" class="live-dashboard__state live-dashboard__state--error">
          {{ store.error }}
        </div>

        <ul v-else class="live-dashboard__event-list">
          <li
            v-for="event in store.items"
            :key="event.id"
            class="live-dashboard__event-item"
          >
            <span class="live-dashboard__event-class">{{ event.action_class }}</span>
            <span class="live-dashboard__event-camera">cam {{ event.camera_id }}</span>
            <span class="badge badge--info">{{ (event.confidence * 100).toFixed(1) }}%</span>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.live-dashboard {
  padding: $spacing-6;

  @include element(title) {
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    margin-bottom: $spacing-6;
  }

  @include element(layout) {
    @include flex(row, flex-start, flex-start, $spacing-6);
  }

  @include element(map-section) {
    position: relative;
    flex: 1;
    min-height: 400px;
    background: rgba($color-text, 0.04);
    border-radius: $border-radius-sm;
    border: 1px solid rgba($color-text, 0.1);
  }

  @include element(events) {
    width: 320px;
    @include flex(column, stretch, flex-start, $spacing-2);
  }

  @include element(state) {
    opacity: 0.5;
    font-size: $font-size-sm;

    @include modifier(error) {
      color: $color-danger;
      opacity: 1;
    }
  }

  @include element(event-list) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(event-item) {
    @include flex(row, center, flex-start, $spacing-2);
    padding: $spacing-2 $spacing-3;
    background: $color-surface;
    border-radius: $border-radius-sm;
    font-size: $font-size-sm;
  }

  @include element(event-class) {
    font-weight: $font-weight-medium;
    flex: 1;
  }

  @include element(event-camera) {
    font-family: $font-family-mono;
    font-size: $font-size-xs;
    opacity: 0.6;
  }
}
</style>
