<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore, useResourceGraphStore } from '../stores/resources.js'

const props = defineProps({
  keyword: {
    type: String,
    required: true,
  },
})

const resourceFilterStore = useResourceFilterStore()
const {
  selectedKeyword,
} = storeToRefs(resourceFilterStore)
const resourceGraphStore = useResourceGraphStore()
const {
  rankedKeywordMap,
} = storeToRefs(resourceGraphStore)


const isActive = computed(() => selectedKeyword.value === props.keyword )
const activeClass = computed(() => isActive.value ? 'active fw-bold text-light-emphasis fs-5' : 'text-light fs-6')
const isDisplayedClass = computed(() => isActive.value || rankedKeywordMap.value.has(props.keyword) ? '' : 'd-none' )
</script>

<template>
  <li class="nav-item" :class="isDisplayedClass">
    <a class="nav-link bg-transparent d-inline-block text-truncate" :class="activeClass"
      @click="useResourceFilterStore().updateSelectedKeyword(keyword)"
      :title="`Keyword: ${keyword}`"
      role="button"
    >{{ keyword }}</a>
  </li>
</template>

<style scoped>
  .nav-link {
    width: 250px;
  }
</style>
