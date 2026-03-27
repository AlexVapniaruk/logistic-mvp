<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useEventsStore } from '~/stores/events.store'
import { useEmployeesStore } from '~/stores/employees.store'
import { useTerminalsStore } from '~/stores/terminals.store'
import { useWebSocket } from '~/composables/useWebSocket'
import { fetchLiveZoneStats } from '~/api-sdk/analytics.api'
import type { WsMessage, Event, SensorPosition, ZoneLiveResponse } from '~/api-sdk/types'

const store = useEventsStore()
const employeesStore = useEmployeesStore()
const terminalsStore = useTerminalsStore()
const { on } = useWebSocket('/ws/live')
const { on: onPosition } = useWebSocket('/ws/positions')

const terminalId = computed(() => terminalsStore.selected?.id)

const employees = computed(() =>
  Object.fromEntries(
    Object.entries(employeesStore.positions).filter(([empId]) => {
      const emp = employeesStore.items.find(e => e.id === Number(empId))
      return emp?.terminal_id === terminalId.value
    })
  )
)

const zoneStats = ref<ZoneLiveResponse | null>(null)

async function refreshZoneStats() {
  zoneStats.value = await fetchLiveZoneStats(5, terminalId.value)
}

onMounted(() => {
  store.loadEvents({ limit: 50 })
  employeesStore.loadEmployees()
  refreshZoneStats()
  on('event', (msg: WsMessage) => store.pushEvent(msg.payload as Event))
  onPosition('position_update', (msg: WsMessage) => {
    employeesStore.updatePosition(msg.payload as SensorPosition)
    refreshZoneStats()
  })
})
</script>

<template>
  <div class="live-dashboard">
    <h1 class="live-dashboard__title">Live Dashboard</h1>

    <div class="live-dashboard__layout">
      <section class="live-dashboard__map-section">
        <EmployeePositionOverlay
          :positions="employees"
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

      <section v-if="zoneStats && zoneStats.zones.length" class="live-dashboard__zones">
        <h2 class="live-dashboard__zones-title">Zone Activity</h2>
        <div
          v-for="zone in zoneStats.zones"
          :key="zone.zone_id"
          class="live-dashboard__zone-card"
        >
          <div class="live-dashboard__zone-header">
            <span class="live-dashboard__zone-name">{{ zone.zone_name }}</span>
            <span class="badge badge--info">{{ zone.active_employee_count }} active</span>
          </div>
          <ul v-if="Object.keys(zone.action_counts).length" class="live-dashboard__zone-actions">
            <li
              v-for="(count, action) in zone.action_counts"
              :key="action"
              class="live-dashboard__zone-action"
            >
              <span>{{ action }}</span>
              <span class="badge badge--secondary">{{ count }}</span>
            </li>
          </ul>
        </div>
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

  @include element(zones) {
    width: 280px;
    @include flex(column, stretch, flex-start, $spacing-3);
  }

  @include element(zones-title) {
    font-size: $font-size-base;
    font-weight: $font-weight-medium;
    opacity: 0.7;
  }

  @include element(zone-card) {
    background: $color-surface;
    border-radius: $border-radius-sm;
    padding: $spacing-3;
    @include flex(column, stretch, flex-start, $spacing-2);
  }

  @include element(zone-header) {
    @include flex(row, center, space-between);
  }

  @include element(zone-name) {
    font-weight: $font-weight-medium;
    font-size: $font-size-sm;
  }

  @include element(zone-actions) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(zone-action) {
    @include flex(row, center, space-between);
    font-size: $font-size-xs;
    opacity: 0.8;
  }
}
</style>
