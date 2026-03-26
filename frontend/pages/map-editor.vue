<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTerminalsStore } from '~/stores/terminals.store'
import { useZonesStore } from '~/stores/zones.store'
import { useSectorsStore } from '~/stores/sectors.store'
import { useCamerasStore } from '~/stores/cameras.store'
import type { Terminal, Zone } from '~/api-sdk/types'

const terminalsStore = useTerminalsStore()
const zonesStore = useZonesStore()
const sectorsStore = useSectorsStore()
const camerasStore = useCamerasStore()

const selectedTerminal = ref<Terminal | null>(null)
const selectedZone = ref<Zone | null>(null)
const drawingMode = ref<'zone' | 'sector' | null>(null)
const newZoneName = ref('')
const newSectorName = ref('')

const mapImageUrl = computed(() => selectedTerminal.value?.map_image_url ?? '')

onMounted(() => terminalsStore.loadTerminals())

async function selectTerminal(terminal: Terminal): Promise<void> {
  selectedTerminal.value = terminal
  selectedZone.value = null
  await zonesStore.loadZones(terminal.id)
}

async function selectZone(zone: Zone): Promise<void> {
  selectedZone.value = zone
  await sectorsStore.loadSectors(zone.id)
}

async function onZonePolygonComplete(points: [number, number][]): Promise<void> {
  if (!selectedTerminal.value || !newZoneName.value) return
  await zonesStore.createZone(selectedTerminal.value.id, { name: newZoneName.value, points })
  newZoneName.value = ''
  drawingMode.value = null
}

async function onSectorPolygonComplete(points: [number, number][]): Promise<void> {
  if (!selectedZone.value || !newSectorName.value) return
  await sectorsStore.createSector(selectedZone.value.id, { name: newSectorName.value, points })
  newSectorName.value = ''
  drawingMode.value = null
}

function handlePolygonComplete(points: [number, number][]): void {
  if (drawingMode.value === 'zone') onZonePolygonComplete(points)
  else if (drawingMode.value === 'sector') onSectorPolygonComplete(points)
}
</script>

<template>
  <div class="map-editor">
    <aside class="map-editor__sidebar">
      <section class="map-editor__section">
        <h2 class="map-editor__heading">Terminals</h2>
        <ul class="map-editor__list">
          <li
            v-for="terminal in terminalsStore.items"
            :key="terminal.id"
            class="map-editor__list-item"
            :class="{ 'map-editor__list-item--active': selectedTerminal?.id === terminal.id }"
            @click="selectTerminal(terminal)"
          >
            {{ terminal.name }}
          </li>
        </ul>
      </section>

      <template v-if="selectedTerminal">
        <section class="map-editor__section">
          <h2 class="map-editor__heading">Zones</h2>
          <ul class="map-editor__list">
            <li
              v-for="zone in zonesStore.items"
              :key="zone.id"
              class="map-editor__list-item"
              :class="{ 'map-editor__list-item--active': selectedZone?.id === zone.id }"
              @click="selectZone(zone)"
            >
              {{ zone.name }}
            </li>
          </ul>
          <div class="map-editor__controls">
            <input v-model="newZoneName" class="map-editor__input" placeholder="Zone name" />
            <button
              class="button button--secondary"
              :disabled="!newZoneName"
              @click="drawingMode = 'zone'"
            >
              Draw zone
            </button>
          </div>
        </section>

        <section v-if="selectedZone" class="map-editor__section">
          <h2 class="map-editor__heading">Sectors in {{ selectedZone.name }}</h2>
          <ul class="map-editor__list">
            <li
              v-for="sector in sectorsStore.items"
              :key="sector.id"
              class="map-editor__list-item"
            >
              {{ sector.name }}
            </li>
          </ul>
          <div class="map-editor__controls">
            <input v-model="newSectorName" class="map-editor__input" placeholder="Sector name" />
            <button
              class="button button--secondary"
              :disabled="!newSectorName"
              @click="drawingMode = 'sector'"
            >
              Draw sector
            </button>
          </div>
        </section>
      </template>

      <div v-if="drawingMode" class="map-editor__mode-indicator">
        Drawing <strong>{{ drawingMode }}</strong> — click canvas, double-click to finish
      </div>
    </aside>

    <main class="map-editor__canvas-area">
      <div v-if="!selectedTerminal" class="map-editor__placeholder">
        Select a terminal to start editing
      </div>
      <div v-else-if="!mapImageUrl" class="map-editor__placeholder">
        No map image — set map_image_url on the terminal
      </div>
      <PolygonCanvas
        v-else
        :image-url="mapImageUrl"
        :polygons="zonesStore.items"
        @polygon-complete="handlePolygonComplete"
      />
    </main>
  </div>
</template>

<style lang="scss" scoped>
.map-editor {
  @include flex(row, stretch, flex-start, 0);
  height: calc(100vh - #{$header-height});

  @include element(sidebar) {
    width: $sidebar-width;
    overflow-y: auto;
    border-right: 1px solid rgba($color-text, 0.1);
    padding: $spacing-4;
    @include flex(column, stretch, flex-start, $spacing-6);
  }

  @include element(section) {
    @include flex(column, stretch, flex-start, $spacing-2);
  }

  @include element(heading) {
    font-size: $font-size-sm;
    font-weight: $font-weight-semibold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.6;
  }

  @include element(list) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(list-item) {
    padding: $spacing-2 $spacing-3;
    border-radius: $border-radius-sm;
    cursor: pointer;
    font-size: $font-size-sm;
    transition: background $transition-fast;

    &:hover {
      background: rgba($color-primary, 0.1);
    }

    @include modifier(active) {
      background: rgba($color-primary, 0.2);
      color: $color-primary;
    }
  }

  @include element(controls) {
    @include flex(column, stretch, flex-start, $spacing-2);
  }

  @include element(input) {
    padding: $spacing-2;
    border: 1px solid rgba($color-text, 0.2);
    border-radius: $border-radius-sm;
    background: $color-surface;
    color: $color-text;
    font-size: $font-size-sm;
  }

  @include element(mode-indicator) {
    padding: $spacing-2 $spacing-3;
    background: rgba($color-primary, 0.1);
    border-radius: $border-radius-sm;
    font-size: $font-size-sm;
    color: $color-primary;
  }

  @include element(canvas-area) {
    flex: 1;
    overflow: auto;
    padding: $spacing-4;
    @include flex(row, flex-start, flex-start, 0);
  }

  @include element(placeholder) {
    margin: auto;
    opacity: 0.4;
    font-size: $font-size-sm;
  }
}
</style>
