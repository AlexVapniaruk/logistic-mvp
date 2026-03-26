<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAnalyticsStore } from '~/stores/analytics.store'
import type { HeatmapResponse, ZoneAnalytics } from '~/api-sdk/types'
import { apiClient } from '~/api-sdk/client'

const store = useAnalyticsStore()
const heatmap = ref<HeatmapResponse | null>(null)
const zoneAnalytics = ref<ZoneAnalytics[]>([])

onMounted(async () => {
  const now = new Date()
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
  store.loadSummary({
    from_ts: weekAgo.toISOString(),
    to_ts: now.toISOString(),
  })
  heatmap.value = await apiClient<HeatmapResponse>('/analytics/heatmap')
  zoneAnalytics.value = await apiClient<ZoneAnalytics[]>('/analytics/zones')
})
</script>

<template>
  <div class="analytics-page">
    <h1 class="analytics-page__title">Analytics</h1>

    <div v-if="store.loading" class="analytics-page__state">Loading…</div>
    <div v-else-if="store.error" class="analytics-page__state analytics-page__state--error">
      {{ store.error }}
    </div>

    <div v-else class="analytics-page__sections">
      <section v-if="store.summary" class="analytics-page__section">
        <h2 class="analytics-page__heading">Event Summary</h2>
        <div class="analytics-page__kpi-grid">
          <div class="card">
            <div class="card__body">
              <p class="analytics-page__kpi-label">Total Events</p>
              <p class="analytics-page__kpi-value">{{ store.summary.total_events }}</p>
            </div>
          </div>
          <div class="card">
            <div class="card__body">
              <p class="analytics-page__kpi-label">Avg Confidence</p>
              <p class="analytics-page__kpi-value">
                {{ (store.summary.avg_confidence * 100).toFixed(1) }}%
              </p>
            </div>
          </div>
        </div>
      </section>

      <section v-if="heatmap?.entries.length" class="analytics-page__section">
        <h2 class="analytics-page__heading">Position Heatmap by Zone</h2>
        <table class="analytics-page__table">
          <thead>
            <tr>
              <th>Zone</th>
              <th>Position count</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in heatmap.entries" :key="entry.zone_id">
              <td>{{ entry.zone_name }}</td>
              <td>{{ entry.count }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section v-if="zoneAnalytics.length" class="analytics-page__section">
        <h2 class="analytics-page__heading">Actions by Zone</h2>
        <table class="analytics-page__table">
          <thead>
            <tr>
              <th>Zone</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="zone in zoneAnalytics" :key="zone.zone_id">
              <td>{{ zone.zone_name }}</td>
              <td>{{ zone.action_count }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.analytics-page {
  padding: $spacing-6;

  @include element(title) {
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    margin-bottom: $spacing-6;
  }

  @include element(state) {
    opacity: 0.5;

    @include modifier(error) {
      color: $color-danger;
      opacity: 1;
    }
  }

  @include element(sections) {
    @include flex(column, stretch, flex-start, $spacing-8);
  }

  @include element(section) {
    @include flex(column, stretch, flex-start, $spacing-3);
  }

  @include element(heading) {
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
  }

  @include element(kpi-grid) {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: $spacing-4;
  }

  @include element(kpi-label) {
    font-size: $font-size-sm;
    opacity: 0.6;
  }

  @include element(kpi-value) {
    font-size: $font-size-3xl;
    font-weight: $font-weight-bold;
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
    }

    td {
      padding: $spacing-2 $spacing-3;
      border-bottom: 1px solid rgba($color-text, 0.08);
    }
  }
}
</style>
