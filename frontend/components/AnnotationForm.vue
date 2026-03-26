<script setup lang="ts">
import { ref } from 'vue'
import type { CameraEvent } from '~/api-sdk/types'

const props = defineProps<{
  event: CameraEvent
  actionTypes: string[]
}>()

const emit = defineEmits<{
  submit: [{ action_type: string; notes: string }]
}>()

const selectedAction = ref(props.actionTypes[0] ?? '')
const notes = ref('')

function handleSubmit(): void {
  if (!selectedAction.value) return
  emit('submit', { action_type: selectedAction.value, notes: notes.value })
  notes.value = ''
}
</script>

<template>
  <div class="annotation-form">
    <div class="annotation-form__meta">
      <span class="badge badge--warning">confidence {{ (event.confidence * 100).toFixed(0) }}%</span>
      <span class="annotation-form__action-type">{{ event.action_type }}</span>
    </div>

    <video
      v-if="event.video_clip_url"
      class="annotation-form__video"
      :src="event.video_clip_url"
      controls
    />

    <div class="annotation-form__field">
      <label class="annotation-form__label">Action type</label>
      <select v-model="selectedAction" class="annotation-form__select">
        <option v-for="at in actionTypes" :key="at" :value="at">{{ at }}</option>
      </select>
    </div>

    <div class="annotation-form__field">
      <label class="annotation-form__label">Notes</label>
      <textarea v-model="notes" class="annotation-form__textarea" rows="3" />
    </div>

    <button class="button button--primary" :disabled="!selectedAction" @click="handleSubmit">
      Submit annotation
    </button>
  </div>
</template>

<style lang="scss" scoped>
.annotation-form {
  @include flex(column, stretch, flex-start, $spacing-4);

  @include element(meta) {
    @include flex(row, center, flex-start, $spacing-2);
  }

  @include element(action-type) {
    font-size: $font-size-sm;
    color: $color-text;
    opacity: 0.7;
  }

  @include element(video) {
    width: 100%;
    border-radius: $border-radius-sm;
    background: #000;
  }

  @include element(field) {
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  @include element(label) {
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
  }

  @include element(select) {
    padding: $spacing-2;
    border: 1px solid rgba($color-text, 0.2);
    border-radius: $border-radius-sm;
    background: $color-surface;
    color: $color-text;
  }

  @include element(textarea) {
    padding: $spacing-2;
    border: 1px solid rgba($color-text, 0.2);
    border-radius: $border-radius-sm;
    background: $color-surface;
    color: $color-text;
    resize: vertical;
  }
}
</style>
