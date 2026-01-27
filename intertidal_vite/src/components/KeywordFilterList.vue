<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceStore } from '../stores/resources.js'
import KeywordFilterListItem from './KeywordFilterListItem.vue'

const resourceDataStore = useResourceStore()
const {
  keywords,
} = storeToRefs(resourceDataStore)
</script>

<template>
  <ul class="nav flex-column">
    <KeywordFilterListItem v-for="keyword in keywords" :keyword="keyword" />
  </ul>
</template>

<style scoped>
</style>