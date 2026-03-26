<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Zone } from '~/api-sdk/types'

const props = defineProps<{
  imageUrl: string
  polygons: Zone[]
}>()

const emit = defineEmits<{
  'polygon-complete': [[number, number][]]
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const currentPoints = ref<[number, number][]>([])

function getRelativePoint(e: MouseEvent): [number, number] {
  const canvas = canvasRef.value!
  const rect = canvas.getBoundingClientRect()
  return [
    (e.clientX - rect.left) * (canvas.width / rect.width),
    (e.clientY - rect.top) * (canvas.height / rect.height),
  ]
}

function handleClick(e: MouseEvent): void {
  currentPoints.value.push(getRelativePoint(e))
  draw()
}

function handleDblClick(): void {
  if (currentPoints.value.length >= 3) {
    emit('polygon-complete', [...currentPoints.value])
  }
  currentPoints.value = []
  draw()
}

function draw(): void {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw saved polygons
  for (const zone of props.polygons) {
    if (!zone.points.length) continue
    ctx.beginPath()
    ctx.moveTo(zone.points[0][0], zone.points[0][1])
    for (const [x, y] of zone.points.slice(1)) ctx.lineTo(x, y)
    ctx.closePath()
    ctx.strokeStyle = '#3b82f6'
    ctx.lineWidth = 2
    ctx.fillStyle = 'rgba(59,130,246,0.15)'
    ctx.fill()
    ctx.stroke()
  }

  // Draw current polygon in progress
  if (currentPoints.value.length > 0) {
    ctx.beginPath()
    ctx.moveTo(currentPoints.value[0][0], currentPoints.value[0][1])
    for (const [x, y] of currentPoints.value.slice(1)) ctx.lineTo(x, y)
    ctx.strokeStyle = '#f59e0b'
    ctx.lineWidth = 2
    ctx.setLineDash([4, 4])
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

onMounted(() => draw())
</script>

<template>
  <div class="polygon-canvas">
    <img :src="imageUrl" class="polygon-canvas__image" alt="Map" @load="draw" />
    <canvas
      ref="canvasRef"
      class="polygon-canvas__overlay"
      width="800"
      height="600"
      @click="handleClick"
      @dblclick.prevent="handleDblClick"
    />
    <p class="polygon-canvas__hint">Click to add points · Double-click to close polygon</p>
  </div>
</template>

<style lang="scss" scoped>
.polygon-canvas {
  position: relative;
  display: inline-block;

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
    color: $color-text;
    opacity: 0.6;
    margin-top: $spacing-1;
  }
}
</style>
