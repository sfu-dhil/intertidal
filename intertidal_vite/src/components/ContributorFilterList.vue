<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceStore } from '../stores/resources.js'
import ContributorFilterListItem from './ContributorFilterListItem.vue'

const resourceDataStore = useResourceStore()
const {
  people,
  organizations,
} = storeToRefs(resourceDataStore)

const unifiedEntityList = computed(() => [...people.value.map((o) => ({...o, type: 'person'})), ...organizations.value.map((o) => ({...o, type: 'organization'}))].sort((a, b) => `${a.label}`.localeCompare(b.label)))
</script>

<template>
  <ul class="nav flex-column">
    <ContributorFilterListItem v-for="entity in unifiedEntityList" :id="entity.id" :type="entity.type" :label="entity.label" />
  </ul>
</template>

<style scoped>
</style>