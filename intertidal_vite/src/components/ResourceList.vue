<script setup>
import { storeToRefs } from 'pinia'
import { useResourceStore } from '../stores/resources.js'
import ResourceListItem from './ResourceListItem.vue'

const resourceDataStore = useResourceStore()
const {
  resources,
} = storeToRefs(resourceDataStore)
</script>

<template>
  <ResourceListItem v-for="resource in resources" :resource="resource" />
</template>

<style scoped>
</style>