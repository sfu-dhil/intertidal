<script setup>
import ResourceListView from './components/ResourceListView.vue'
import LoadingDots from './components/LoadingDots.vue'

</script>

<template>
  <div class="position-relative">
    <Suspense>
      <ResourceListView />
      <template #fallback><LoadingDots /></template>
    </Suspense>
  </div>
</template>

<style scoped>
</style>