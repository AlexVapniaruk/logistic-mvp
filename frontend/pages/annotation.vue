<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCameraEventsStore } from '~/stores/camera-events.store'
import { useAnnotationsStore } from '~/stores/annotations.store'
import type { CameraEvent } from '~/api-sdk/types'

const ACTION_TYPES = ['picking', 'idle', 'walking', 'loading', 'unloading']

const cameraEventsStore = useCameraEventsStore()
const annotationsStore = useAnnotationsStore()

const selected = ref<CameraEvent | null>(null)

onMounted(() => cameraEventsStore.loadAnnotationQueue())

async function handleAnnotationSubmit(payload: { action_type: string; notes: string }): Promise<void> {
  if (!selected.value) return
  await annotationsStore.submitAnnotation({
    camera_event_id: selected.value.id,
    annotator_id: 'annotator',
    action_type: payload.action_type,
    notes: payload.notes || null,
  })
  selected.value = null
}
</script>

<template>
  <div class="annotation-page">
    <div class="annotation-page__queue">
      <h2 class="annotation-page__heading">Annotation Queue ({{ cameraEventsStore.annotationQueue.length }})</h2>

      <div v-if="cameraEventsStore.loading" class="annotation-page__state">Loading…</div>
      <div v-else-if="!cameraEventsStore.annotationQueue.length" class="annotation-page__state">
        Queue is empty
      </div>

      <ul v-else class="annotation-page__list">
        <li
          v-for="event in cameraEventsStore.annotationQueue"
          :key="event.id"
          class="annotation-page__list-item"
          :class="{ 'annotation-page__list-item--selected': selected?.id === event.id }"
          @click="selected = event"
        >
          <span class="badge badge--warning">{{ (event.confidence * 100).toFixed(0) }}%</span>
          <span class="annotation-page__event-type">{{ event.action_type }}</span>
          <span class="annotation-page__event-ts">{{ new Date(event.timestamp).toLocaleTimeString() }}</span>
        </li>
      </ul>
    </div>

    <div class="annotation-page__detail">
      <div v-if="!selected" class="annotation-page__state">Select an event to annotate</div>
      <AnnotationForm
        v-else
        :event="selected"
        :action-types="ACTION_TYPES"
        @submit="handleAnnotationSubmit"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.annotation-page {
  @include flex(row, stretch, flex-start, 0);
  height: calc(100vh - #{$header-height});

  @include element(queue) {
    width: 320px;
    border-right: 1px solid rgba($color-text, 0.1);
    padding: $spacing-4;
    overflow-y: auto;
    @include flex(column, stretch, flex-start, $spacing-3);
  }

  @include element(heading) {
    font-size: $font-size-base;
    font-weight: $font-weight-semibold;
  }

  @include element(list) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(list-item) {
    @include flex(row, center, flex-start, $spacing-2);
    padding: $spacing-2 $spacing-3;
    border-radius: $border-radius-sm;
    cursor: pointer;
    transition: background $transition-fast;

    &:hover {
      background: rgba($color-primary, 0.08);
    }

    @include modifier(selected) {
      background: rgba($color-primary, 0.15);
    }
  }

  @include element(event-type) {
    flex: 1;
    font-size: $font-size-sm;
  }

  @include element(event-ts) {
    font-size: $font-size-xs;
    font-family: $font-family-mono;
    opacity: 0.5;
  }

  @include element(detail) {
    flex: 1;
    padding: $spacing-6;
    overflow-y: auto;
  }

  @include element(state) {
    opacity: 0.4;
    font-size: $font-size-sm;
    text-align: center;
    padding: $spacing-8 0;
  }
}
</style>
