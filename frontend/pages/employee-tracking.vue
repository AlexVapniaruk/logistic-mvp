<script setup lang="ts">
import { onMounted } from 'vue'
import { useEmployeesStore } from '~/stores/employees.store'

const store = useEmployeesStore()

onMounted(() => store.loadEmployees())
</script>

<template>
  <div class="employee-tracking">
    <h1 class="employee-tracking__title">Employee Tracking</h1>

    <div v-if="store.loading" class="employee-tracking__state">Loading…</div>
    <div v-else-if="store.error" class="employee-tracking__state employee-tracking__state--error">
      {{ store.error }}
    </div>

    <div v-else class="employee-tracking__grid">
      <EmployeeCard
        v-for="employee in store.items"
        :key="employee.id"
        :employee="employee"
        :position="store.positions[employee.id] ?? null"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.employee-tracking {
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

  @include element(grid) {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: $spacing-4;
  }
}
</style>
