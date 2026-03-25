<script setup lang="ts">
import { onMounted } from 'vue'
import { useAnalyticsStore } from '~/stores/analytics.store'

const store = useAnalyticsStore()

onMounted(() => {
  const now = new Date()
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
  store.loadSummary({
    from_ts: weekAgo.toISOString(),
    to_ts: now.toISOString(),
  })
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Analytics</h1>

    <div v-if="store.loading" class="text-gray-500">Loading...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>

    <div v-else-if="store.summary" class="grid grid-cols-2 gap-4">
      <div class="border rounded p-4">
        <p class="text-sm text-gray-500">Total Events</p>
        <p class="text-3xl font-bold">{{ store.summary.total_events }}</p>
      </div>
      <div class="border rounded p-4">
        <p class="text-sm text-gray-500">Avg Confidence</p>
        <p class="text-3xl font-bold">{{ (store.summary.avg_confidence * 100).toFixed(1) }}%</p>
      </div>
    </div>
  </div>
</template>
