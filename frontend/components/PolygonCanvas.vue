<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import type { Zone, Sector } from '~/api-sdk/types'

const props = defineProps<{
  imageUrl: string
  zones: Zone[]
  sectors: Sector[]
  selectedZoneId: number | null
  drawingMode: 'zone' | 'sector' | null
}>()

const emit = defineEmits<{
  'polygon-complete': [[number, number][]]
  'zone-click': [number]
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const currentPoints = ref<[number, number][]>([])

// ---------------------------------------------------------------------------
// Point-in-polygon (ray casting) — used for zone click detection
// ---------------------------------------------------------------------------
function isPointInPolygon(x: number, y: number, points: [number, number][]): boolean {
  let inside = false
  let j = points.length - 1
  for (let i = 0; i < points.length; j = i++) {
    const [xi, yi] = points[i]
    const [xj, yj] = points[j]
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) {
      inside = !inside
    }
  }
  return inside
}

// ---------------------------------------------------------------------------
// Coordinate helpers
// ---------------------------------------------------------------------------
function getCanvasPoint(e: MouseEvent): [number, number] {
  const canvas = canvasRef.value!
  const rect = canvas.getBoundingClientRect()
  return [
    (e.clientX - rect.left) * (canvas.width / rect.width),
    (e.clientY - rect.top) * (canvas.height / rect.height),
  ]
}

// ---------------------------------------------------------------------------
// Event handlers
// ---------------------------------------------------------------------------
function handleClick(e: MouseEvent): void {
  const [x, y] = getCanvasPoint(e)

  if (props.drawingMode !== null) {
    currentPoints.value.push([x, y])
    draw()
    return
  }

  // Selection mode — find clicked zone
  for (const zone of props.zones) {
    if (isPointInPolygon(x, y, zone.points as [number, number][])) {
      emit('zone-click', zone.id)
      return
    }
  }
}

function handleDblClick(): void {
  if (props.drawingMode === null) return
  if (currentPoints.value.length >= 3) {
    emit('polygon-complete', [...currentPoints.value])
  }
  currentPoints.value = []
  draw()
}

// ---------------------------------------------------------------------------
// Drawing
// ---------------------------------------------------------------------------
function drawPolygon(
  ctx: CanvasRenderingContext2D,
  points: [number, number][],
  stroke: string,
  fill: string,
  lineWidth = 2,
): void {
  if (!points.length) return
  ctx.beginPath()
  ctx.moveTo(points[0][0], points[0][1])
  for (const [x, y] of points.slice(1)) ctx.lineTo(x, y)
  ctx.closePath()
  ctx.strokeStyle = stroke
  ctx.fillStyle = fill
  ctx.lineWidth = lineWidth
  ctx.fill()
  ctx.stroke()
}

function draw(): void {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Zones
  for (const zone of props.zones) {
    const isSelected = zone.id === props.selectedZoneId
    drawPolygon(
      ctx,
      zone.points as [number, number][],
      isSelected ? '#2563eb' : '#3b82f6',
      isSelected ? 'rgba(37,99,235,0.25)' : 'rgba(59,130,246,0.12)',
      isSelected ? 3 : 2,
    )

    // Zone label
    if (zone.points.length) {
      const xs = zone.points.map(p => p[0])
      const ys = zone.points.map(p => p[1])
      const cx = (Math.min(...xs) + Math.max(...xs)) / 2
      const cy = (Math.min(...ys) + Math.max(...ys)) / 2
      ctx.font = '12px Inter, sans-serif'
      ctx.fillStyle = isSelected ? '#2563eb' : 'rgba(59,130,246,0.9)'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(zone.name, cx, cy)
    }
  }

  // Sectors (green)
  for (const sector of props.sectors) {
    drawPolygon(
      ctx,
      sector.points as [number, number][],
      '#16a34a',
      'rgba(22,163,74,0.18)',
      1.5,
    )

    if (sector.points.length) {
      const xs = sector.points.map(p => p[0])
      const ys = sector.points.map(p => p[1])
      const cx = (Math.min(...xs) + Math.max(...xs)) / 2
      const cy = (Math.min(...ys) + Math.max(...ys)) / 2
      ctx.font = '11px Inter, sans-serif'
      ctx.fillStyle = 'rgba(22,163,74,0.9)'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(sector.name, cx, cy)
    }
  }

  // Current polygon in progress (amber dashed)
  if (currentPoints.value.length > 0) {
    ctx.beginPath()
    ctx.moveTo(currentPoints.value[0][0], currentPoints.value[0][1])
    for (const [x, y] of currentPoints.value.slice(1)) ctx.lineTo(x, y)
    ctx.strokeStyle = '#f59e0b'
    ctx.lineWidth = 2
    ctx.setLineDash([5, 4])
    ctx.stroke()
    ctx.setLineDash([])

    for (const [x, y] of currentPoints.value) {
      ctx.beginPath()
      ctx.arc(x, y, 4, 0, Math.PI * 2)
      ctx.fillStyle = '#f59e0b'
      ctx.fill()
    }
  }
}

watch(() => [props.zones, props.sectors, props.selectedZoneId], () => draw(), { deep: true })
onMounted(() => draw())
</script>

<template>
  <div class="polygon-canvas">
    <img :src="imageUrl" class="polygon-canvas__image" alt="Terminal map" @load="draw" />
    <canvas
      ref="canvasRef"
      class="polygon-canvas__overlay"
      width="800"
      height="600"
      @click="handleClick"
      @dblclick.prevent="handleDblClick"
    />
    <p class="polygon-canvas__hint">
      <template v-if="drawingMode">
        Drawing <strong>{{ drawingMode }}</strong> — click to add points, double-click to finish
      </template>
      <template v-else>
        Click on a zone to select it
      </template>
    </p>
  </div>
</template>

<style lang="scss" scoped>
.polygon-canvas {
  position: relative;
  display: inline-block;
  user-select: none;

  @include element(image) {
    display: block;
    max-width: 100%;
  }

  @include element(overlay) {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    cursor: crosshair;
  }

  @include element(hint) {
    font-size: $font-size-xs;
    opacity: 0.55;
    margin-top: $spacing-1;
  }
}
</style>
