<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useTerminalsStore } from '~/stores/terminals.store'

const terminalsStore = useTerminalsStore()
const terminal = computed(() => terminalsStore.selected)

const navLinks = computed(() => [
  { to: '/live-dashboard',    label: 'Live Dashboard',  icon: '●' },
  { to: terminal.value ? `/terminals/${terminal.value.id}` : '/terminals', label: 'Map Editor', icon: '⊞' },
  { to: '/cameras',           label: 'Cameras',         icon: '◉' },
  { to: '/employee-tracking', label: 'Employees',       icon: '♟' },
  { to: '/annotation',        label: 'Annotation',      icon: '✎' },
  { to: '/analytics',         label: 'Analytics',       icon: '↗' },
  { to: '/training',          label: 'Training',        icon: '⚙' },
])

// Restore terminal from localStorage on first mount if store is empty
onMounted(async () => {
  if (!terminalsStore.selected) {
    const savedId = import.meta.client && localStorage.getItem('selectedTerminalId')
    if (savedId) {
      if (!terminalsStore.items.length) await terminalsStore.loadTerminals()
      const found = terminalsStore.items.find(t => t.id === Number(savedId))
      if (found) terminalsStore.selectTerminal(found)
    }
  }
})
</script>

<template>
  <div class="layout">
    <header class="layout__header">
      <span class="layout__logo">Logistics Terminal</span>

      <div class="layout__terminal-badge" v-if="terminal">
        <span class="layout__terminal-name">{{ terminal.name }}</span>
        <NuxtLink to="/terminals" class="layout__switch" @click="terminalsStore.clearTerminal()">
          Switch
        </NuxtLink>
      </div>
      <NuxtLink v-else to="/terminals" class="layout__select-btn">
        Select Terminal
      </NuxtLink>
    </header>

    <nav class="layout__sidebar">
      <ul class="layout__nav">
        <li v-for="link in navLinks" :key="link.to">
          <NuxtLink :to="link.to" class="layout__nav-link">
            <span class="layout__nav-icon">{{ link.icon }}</span>
            <span>{{ link.label }}</span>
          </NuxtLink>
        </li>
      </ul>
    </nav>

    <main class="layout__main">
      <slot />
    </main>
  </div>
</template>

<style lang="scss" scoped>
.layout {
  &__logo {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: $color-primary;
    letter-spacing: -0.02em;
  }

  &__terminal-badge {
    @include flex(row, center, flex-start, $spacing-3);
    margin-left: $spacing-4;
    padding: $spacing-1 $spacing-3;
    background: rgba($color-primary, 0.08);
    border-radius: $border-radius-sm;
    border: 1px solid rgba($color-primary, 0.2);
  }

  &__terminal-name {
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    color: $color-primary;
  }

  &__switch {
    font-size: $font-size-xs;
    color: $color-text-muted;
    text-decoration: none;
    opacity: 0.7;
    &:hover { opacity: 1; }
  }

  &__select-btn {
    margin-left: $spacing-4;
    font-size: $font-size-sm;
    color: $color-primary;
    text-decoration: none;
    opacity: 0.8;
    &:hover { opacity: 1; }
  }

  &__nav {
    list-style: none;
    padding: 0 $spacing-3;
    @include flex(column, stretch, flex-start, $spacing-1);
  }

  &__nav-link {
    @include flex(row, center, flex-start, $spacing-3);
    padding: $spacing-2 $spacing-3;
    border-radius: $border-radius-sm;
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    color: $color-text-muted;
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: background $transition-fast, color $transition-fast, border-color $transition-fast;

    &:hover {
      background: rgba($color-primary, 0.06);
      color: $color-text;
    }

    &.router-link-active {
      background: rgba($color-primary, 0.1);
      color: $color-primary;
      border-left-color: $color-primary;
    }
  }

  &__nav-icon {
    width: 18px;
    text-align: center;
    font-size: $font-size-xs;
    opacity: 0.8;
  }
}
</style>
