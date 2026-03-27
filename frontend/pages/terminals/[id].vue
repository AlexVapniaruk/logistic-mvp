<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTerminalsStore } from '~/stores/terminals.store'
import { useZonesStore } from '~/stores/zones.store'
import { useSectorsStore } from '~/stores/sectors.store'
import { useCamerasStore } from '~/stores/cameras.store'
import type { Zone } from '~/api-sdk/types'

const route = useRoute()
const terminalId = Number(route.params.id)

const terminalsStore = useTerminalsStore()
const zonesStore = useZonesStore()
const sectorsStore = useSectorsStore()
const camerasStore = useCamerasStore()

// — state —
const selectedZone = ref<Zone | null>(null)
const drawingMode = ref<'zone' | 'sector' | null>(null)
const newZoneName = ref('')
const newSectorName = ref('')
const mapUrlInput = ref('')
const savingMap = ref(false)

// — computed —
const terminal = computed(() => terminalsStore.selected)
const mapImageUrl = computed(() => terminal.value?.map_image_url ?? '')

const zoneCameras = computed(() =>
  selectedZone.value
    ? camerasStore.items.filter(c => c.zone_id === selectedZone.value!.id)
    : []
)

// — lifecycle —
onMounted(async () => {
  await terminalsStore.loadTerminal(terminalId)
  mapUrlInput.value = terminal.value?.map_image_url ?? ''
  await Promise.all([
    zonesStore.loadZones(terminalId),
    camerasStore.loadCameras(),
  ])
})

// — zone actions —
async function selectZone(zone: Zone): Promise<void> {
  selectedZone.value = zone
  drawingMode.value = null
  await sectorsStore.loadSectors(zone.id)
}

function onZoneClick(zoneId: number): void {
  const zone = zonesStore.items.find(z => z.id === zoneId)
  if (zone) selectZone(zone)
}

// — drawing —
async function onPolygonComplete(points: [number, number][]): Promise<void> {
  if (drawingMode.value === 'zone') {
    if (!newZoneName.value) return
    await zonesStore.createZone(terminalId, { name: newZoneName.value, points })
    newZoneName.value = ''
  } else if (drawingMode.value === 'sector') {
    if (!selectedZone.value || !newSectorName.value) return
    await sectorsStore.createSector(selectedZone.value.id, { name: newSectorName.value, points })
    newSectorName.value = ''
  }
  drawingMode.value = null
}

function startDrawing(mode: 'zone' | 'sector'): void {
  drawingMode.value = mode
}

// — map image —
async function saveMapUrl(): Promise<void> {
  if (!mapUrlInput.value.trim()) return
  savingMap.value = true
  try {
    await terminalsStore.updateTerminal(terminalId, { map_image_url: mapUrlInput.value.trim() })
  } finally {
    savingMap.value = false
  }
}

async function onFileChange(e: Event): Promise<void> {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  savingMap.value = true
  try {
    await terminalsStore.uploadImage(terminalId, file)
    mapUrlInput.value = terminal.value?.map_image_url ?? ''
    ;(e.target as HTMLInputElement).value = ''
  } finally {
    savingMap.value = false
  }
}
</script>

<template>
  <div class="terminal-map">

    <!-- Top bar -->
    <header class="terminal-map__topbar">
      <NuxtLink to="/terminals" class="terminal-map__back">← Terminals</NuxtLink>
      <h1 class="terminal-map__title">{{ terminal?.name ?? '…' }}</h1>
      <div class="terminal-map__map-controls">
        <input
          v-model="mapUrlInput"
          class="terminal-map__url-input"
          placeholder="Map image URL or upload →"
          @keydown.enter="saveMapUrl"
        />
        <label class="button button--secondary button--sm terminal-map__file-label">
          Upload
          <input type="file" accept="image/*" class="terminal-map__file-input" @change="onFileChange" />
        </label>
        <button
          class="button button--primary button--sm"
          :disabled="savingMap"
          @click="saveMapUrl"
        >
          Set
        </button>
      </div>
    </header>

    <div class="terminal-map__body">

      <!-- Sidebar -->
      <aside class="terminal-map__sidebar">

        <!-- Zones -->
        <section class="terminal-map__section">
          <h2 class="terminal-map__heading">Zones</h2>

          <ul class="terminal-map__list">
            <li
              v-for="zone in zonesStore.items"
              :key="zone.id"
              class="terminal-map__list-item"
              :class="{ 'terminal-map__list-item--active': selectedZone?.id === zone.id }"
              @click="selectZone(zone)"
            >
              {{ zone.name }}
            </li>
          </ul>

          <div class="terminal-map__add-row">
            <input
              v-model="newZoneName"
              class="terminal-map__input"
              placeholder="Zone name"
              @keydown.enter="newZoneName && startDrawing('zone')"
            />
            <button
              class="button button--secondary button--sm"
              :disabled="!newZoneName || drawingMode === 'zone'"
              @click="startDrawing('zone')"
            >
              Draw
            </button>
          </div>
        </section>

        <!-- Sectors (when zone selected) -->
        <section v-if="selectedZone" class="terminal-map__section">
          <h2 class="terminal-map__heading">
            Sectors
            <span class="terminal-map__zone-tag">{{ selectedZone.name }}</span>
          </h2>

          <p v-if="!sectorsStore.items.length" class="terminal-map__empty">No sectors yet.</p>
          <ul v-else class="terminal-map__list">
            <li
              v-for="sector in sectorsStore.items"
              :key="sector.id"
              class="terminal-map__list-item terminal-map__list-item--sector"
            >
              {{ sector.name }}
            </li>
          </ul>

          <div class="terminal-map__add-row">
            <input
              v-model="newSectorName"
              class="terminal-map__input"
              placeholder="Sector name"
              @keydown.enter="newSectorName && startDrawing('sector')"
            />
            <button
              class="button button--secondary button--sm"
              :disabled="!newSectorName || drawingMode === 'sector'"
              @click="startDrawing('sector')"
            >
              Draw
            </button>
          </div>
        </section>

        <!-- Cameras in selected zone -->
        <section v-if="selectedZone && zoneCameras.length" class="terminal-map__section">
          <h2 class="terminal-map__heading">Cameras</h2>
          <ul class="terminal-map__list">
            <li
              v-for="cam in zoneCameras"
              :key="cam.id"
              class="terminal-map__list-item terminal-map__list-item--camera"
            >
              <span>{{ cam.name }}</span>
              <span v-if="cam.location" class="terminal-map__cam-loc">{{ cam.location }}</span>
            </li>
          </ul>
        </section>

        <!-- Drawing indicator -->
        <div v-if="drawingMode" class="terminal-map__drawing-hint">
          Drawing <strong>{{ drawingMode }}</strong><br />
          <span>Click to add points · Double-click to finish</span>
        </div>
      </aside>

      <!-- Canvas area -->
      <main class="terminal-map__canvas">
        <div v-if="!mapImageUrl" class="terminal-map__placeholder">
          <p>No map image set.</p>
          <p>Paste a URL or upload an image above.</p>
        </div>
        <PolygonCanvas
          v-else
          :image-url="mapImageUrl"
          :zones="zonesStore.items"
          :sectors="sectorsStore.items"
          :selected-zone-id="selectedZone?.id ?? null"
          :drawing-mode="drawingMode"
          @polygon-complete="onPolygonComplete"
          @zone-click="onZoneClick"
        />
      </main>

    </div>
  </div>
</template>

<style lang="scss" scoped>
.terminal-map {
  display: grid;
  grid-template-rows: auto 1fr;
  height: calc(100vh - #{$header-height});
  overflow: hidden;

  @include element(topbar) {
    @include flex(row, center, flex-start, $spacing-4);
    padding: $spacing-3 $spacing-6;
    border-bottom: 1px solid $color-border;
    background: $color-surface;
    flex-shrink: 0;
  }

  @include element(back) {
    font-size: $font-size-sm;
    color: $color-primary;
    text-decoration: none;
    white-space: nowrap;
    opacity: 0.8;
    &:hover { opacity: 1; }
  }

  @include element(title) {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    flex: 1;
    @include truncate;
  }

  @include element(map-controls) {
    @include flex(row, center, flex-start, $spacing-2);
  }

  @include element(url-input) {
    padding: $spacing-1 $spacing-2;
    border: 1px solid $color-border;
    border-radius: $border-radius-sm;
    background: $color-bg;
    color: $color-text;
    font-size: $font-size-sm;
    width: 260px;
  }

  @include element(file-label) {
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  @include element(file-input) {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  @include element(body) {
    @include flex(row, stretch, flex-start, 0);
    overflow: hidden;
  }

  @include element(sidebar) {
    width: 220px;
    flex-shrink: 0;
    overflow-y: auto;
    border-right: 1px solid $color-border;
    padding: $spacing-4;
    @include flex(column, stretch, flex-start, $spacing-5);
    background: $color-surface;
  }

  @include element(section) {
    @include flex(column, stretch, flex-start, $spacing-2);
  }

  @include element(heading) {
    font-size: $font-size-xs;
    font-weight: $font-weight-semibold;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.5;
    @include flex(row, center, flex-start, $spacing-2);
  }

  @include element(zone-tag) {
    font-size: $font-size-xs;
    background: rgba($color-primary, 0.1);
    color: $color-primary;
    padding: 1px $spacing-1;
    border-radius: $border-radius-sm;
    text-transform: none;
    letter-spacing: 0;
    font-weight: $font-weight-medium;
    @include truncate;
    max-width: 90px;
  }

  @include element(list) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(list-item) {
    padding: $spacing-1 $spacing-2;
    border-radius: $border-radius-sm;
    cursor: pointer;
    font-size: $font-size-sm;
    transition: background $transition-fast;

    &:hover { background: rgba($color-primary, 0.07); }

    @include modifier(active) {
      background: rgba($color-primary, 0.15);
      color: $color-primary;
      font-weight: $font-weight-medium;
    }

    @include modifier(sector) {
      cursor: default;
      color: #16a34a;
      font-size: $font-size-xs;
      padding-left: $spacing-3;
      &:hover { background: rgba(22, 163, 74, 0.07); }
    }

    @include modifier(camera) {
      cursor: default;
      @include flex(row, baseline, space-between, $spacing-1);
      font-size: $font-size-xs;
    }
  }

  @include element(cam-loc) {
    opacity: 0.5;
    font-size: $font-size-xs;
    @include truncate;
    max-width: 80px;
  }

  @include element(add-row) {
    @include flex(row, center, flex-start, $spacing-1);
  }

  @include element(input) {
    flex: 1;
    padding: $spacing-1 $spacing-2;
    border: 1px solid $color-border;
    border-radius: $border-radius-sm;
    background: $color-bg;
    color: $color-text;
    font-size: $font-size-sm;
    min-width: 0;
  }

  @include element(empty) {
    font-size: $font-size-xs;
    opacity: 0.4;
  }

  @include element(drawing-hint) {
    padding: $spacing-2;
    background: rgba($color-warning, 0.12);
    border-radius: $border-radius-sm;
    font-size: $font-size-xs;
    color: #92400e;
    line-height: 1.5;
  }

  @include element(canvas) {
    flex: 1;
    overflow: auto;
    padding: $spacing-4;
    background: $color-bg;
    @include flex(row, flex-start, flex-start, 0);
  }

  @include element(placeholder) {
    margin: auto;
    text-align: center;
    opacity: 0.35;
    font-size: $font-size-sm;
    line-height: 1.8;
  }
}
</style>
