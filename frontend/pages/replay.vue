<script setup lang="ts">
import { useVideoPlayer } from '~/composables/useVideoPlayer'

const { videoRef, isPlaying, currentTime, play, pause, seekTo } = useVideoPlayer()
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Replay</h1>

    <video
      ref="videoRef"
      class="w-full rounded shadow"
      controls
    />

    <div class="mt-4 flex gap-2">
      <button
        class="px-4 py-2 bg-blue-600 text-white rounded"
        @click="isPlaying ? pause() : play()"
      >
        {{ isPlaying ? 'Pause' : 'Play' }}
      </button>
      <span class="text-sm text-gray-600 self-center">{{ currentTime.toFixed(1) }}s</span>
    </div>
  </div>
</template>
