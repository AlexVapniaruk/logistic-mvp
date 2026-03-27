<script setup lang="ts">
import { onMounted } from 'vue'
import { useTerminalsStore } from '~/stores/terminals.store'
import type { Terminal } from '~/api-sdk/types'

definePageMeta({ layout: false })

const store = useTerminalsStore()

onMounted(() => store.loadTerminals())

async function select(terminal: Terminal): Promise<void> {
  store.selectTerminal(terminal)
  await navigateTo('/live-dashboard')
}
</script>

<template>
  <div class="terminal-picker">
    <div class="terminal-picker__inner">
      <div class="terminal-picker__brand">
        <span class="terminal-picker__logo">Logistics Terminal</span>
        <p class="terminal-picker__sub">Select a terminal to continue</p>
      </div>

      <div v-if="store.loading" class="terminal-picker__state">Loading terminals…</div>
      <div v-else-if="store.error" class="terminal-picker__state terminal-picker__state--error">
        {{ store.error }}
      </div>
      <p v-else-if="!store.items.length" class="terminal-picker__state">
        No terminals found. Create one via the API.
      </p>

      <ul v-else class="terminal-picker__grid">
        <li
          v-for="terminal in store.items"
          :key="terminal.id"
          class="terminal-picker__card"
          @click="select(terminal)"
        >
          <div class="terminal-picker__card-icon">▦</div>
          <div class="terminal-picker__card-body">
            <p class="terminal-picker__card-name">{{ terminal.name }}</p>
            <p v-if="terminal.description" class="terminal-picker__card-desc">
              {{ terminal.description }}
            </p>
          </div>
          <span class="terminal-picker__card-arrow">→</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.terminal-picker {
  min-height: 100vh;
  background: $color-bg;
  @include flex(row, center, center, 0);

  @include element(inner) {
    width: 100%;
    max-width: 520px;
    padding: $spacing-16 $spacing-6;
    @include flex(column, stretch, flex-start, $spacing-8);
  }

  @include element(brand) {
    @include flex(column, flex-start, flex-start, $spacing-2);
  }

  @include element(logo) {
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    color: $color-primary;
    letter-spacing: -0.03em;
  }

  @include element(sub) {
    font-size: $font-size-sm;
    opacity: 0.5;
  }

  @include element(state) {
    opacity: 0.5;
    font-size: $font-size-sm;

    @include modifier(error) {
      color: $color-danger;
      opacity: 1;
    }
  }

  @include element(grid) {
    list-style: none;
    @include flex(column, stretch, flex-start, $spacing-3);
  }

  @include element(card) {
    @include flex(row, center, flex-start, $spacing-4);
    padding: $spacing-5;
    background: $color-surface;
    border: 1px solid $color-border;
    border-radius: $border-radius-lg;
    cursor: pointer;
    transition: border-color $transition-fast, box-shadow $transition-fast, transform $transition-fast;

    &:hover {
      border-color: $color-primary;
      box-shadow: $shadow-lg;
      transform: translateY(-1px);
    }
  }

  @include element(card-icon) {
    font-size: $font-size-2xl;
    opacity: 0.4;
    flex-shrink: 0;
  }

  @include element(card-body) {
    flex: 1;
    @include flex(column, flex-start, flex-start, $spacing-1);
  }

  @include element(card-name) {
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
  }

  @include element(card-desc) {
    font-size: $font-size-sm;
    opacity: 0.5;
  }

  @include element(card-arrow) {
    font-size: $font-size-lg;
    opacity: 0.3;
    flex-shrink: 0;
  }
}
</style>
