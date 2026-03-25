<script setup lang="ts">
import { onMounted } from 'vue'
import { useEventsStore } from '~/stores/events.store'
import { useWebSocket } from '~/composables/useWebSocket'
import type { WsMessage, Event } from '~/api-sdk/types'

const store = useEventsStore()
const { on } = useWebSocket('/ws/live')

onMounted(() => {
  store.loadEvents({ limit: 50 })
  on('event', (msg: WsMessage) => store.pushEvent(msg.payload as Event))
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Live Dashboard</h1>

    <div v-if="store.loading" class="text-gray-500">Connecting...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>

    <ul v-else class="space-y-2">
      <li
        v-for="event in store.items"
        :key="event.id"
        class="border rounded p-3 text-sm"
      >
        <span class="font-medium">{{ event.action_class }}</span>
        — {{ event.camera_id }} ({{ (event.confidence * 100).toFixed(1) }}%)
      </li>
    </ul>
  </div>
</template>
