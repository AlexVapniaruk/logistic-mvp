<script setup lang="ts">
import { onMounted } from 'vue'
import { useTrainingStore } from '~/stores/training.store'

const store = useTrainingStore()

onMounted(() => store.loadModels())
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Model Training</h1>

    <div v-if="store.loading" class="text-gray-500">Loading...</div>
    <div v-else-if="store.error" class="text-red-500">{{ store.error }}</div>

    <div v-else>
      <p class="mb-2 text-sm text-gray-600">Active model: {{ store.activeModel?.name ?? '—' }}</p>
      <!-- Training UI goes here -->
    </div>
  </div>
</template>
