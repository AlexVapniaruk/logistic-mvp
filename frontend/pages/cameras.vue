<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCamerasStore } from '~/stores/cameras.store'
import { useTerminalsStore } from '~/stores/terminals.store'

const store = useCamerasStore()
const terminalsStore = useTerminalsStore()

const cameras = computed(() =>
  store.items.filter(c => c.terminal_id === terminalsStore.selected?.id)
)

onMounted(() => store.loadCameras())
</script>

<template>
  <div class="cameras-page">
    <h1 class="cameras-page__title">Cameras</h1>

    <div v-if="store.loading" class="cameras-page__state">Loading…</div>
    <div v-else-if="store.error" class="cameras-page__state cameras-page__state--error">
      {{ store.error }}
    </div>

    <template v-else>
      <p v-if="!cameras.length" class="cameras-page__state">No cameras for this terminal.</p>

      <table v-else-if="cameras.length" class="cameras-page__table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>MAC</th>
            <th>Version</th>
            <th>Stream URL</th>
            <th>Terminal</th>
            <th>Zone</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="camera in cameras" :key="camera.id">
            <td class="cameras-page__id">{{ camera.id }}</td>
            <td class="cameras-page__name">{{ camera.name }}</td>
            <td>{{ camera.location ?? '—' }}</td>
            <td class="cameras-page__mono">{{ camera.mac_address ?? '—' }}</td>
            <td>
              <span v-if="camera.version" class="badge badge--secondary">{{ camera.version }}</span>
              <span v-else>—</span>
            </td>
            <td class="cameras-page__url">{{ camera.stream_url }}</td>
            <td class="cameras-page__mono">{{ camera.terminal_id }}</td>
            <td class="cameras-page__mono">{{ camera.zone_id ?? '—' }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </div>
</template>

<style lang="scss" scoped>
.cameras-page {
  padding: $spacing-6;

  @include element(title) {
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    margin-bottom: $spacing-6;
  }

  @include element(state) {
    opacity: 0.5;
    font-size: $font-size-sm;

    @include modifier(error) {
      color: $color-danger;
      opacity: 1;
    }
  }

  @include element(table) {
    width: 100%;
    border-collapse: collapse;
    font-size: $font-size-sm;

    th {
      text-align: left;
      padding: $spacing-2 $spacing-3;
      border-bottom: 2px solid rgba($color-text, 0.15);
      font-weight: $font-weight-semibold;
      opacity: 0.7;
      white-space: nowrap;
    }

    td {
      padding: $spacing-2 $spacing-3;
      border-bottom: 1px solid rgba($color-text, 0.08);
      vertical-align: middle;
    }
  }

  @include element(id) {
    font-family: $font-family-mono;
    font-size: $font-size-xs;
    opacity: 0.5;
    width: 48px;
  }

  @include element(name) {
    font-weight: $font-weight-medium;
  }

  @include element(mono) {
    font-family: $font-family-mono;
    font-size: $font-size-xs;
  }

  @include element(url) {
    font-family: $font-family-mono;
    font-size: $font-size-xs;
    @include truncate;
    max-width: 200px;
  }
}
</style>
