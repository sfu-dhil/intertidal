<script setup>
import { useTemplateRef, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore } from '../stores/resources.js'
import { useElementBounding } from '@vueuse/core'

const resourceFilterStore = useResourceFilterStore()
const {
  selectedKey,
} = storeToRefs(resourceFilterStore)

const props = defineProps({
  category: {
    type: Object,
    required: true,
  },
})
const categoryCoordinateMap = defineModel('categoryCoordinateMap', { default: new Map() })

const itemEl = useTemplateRef('itemEl')
const { top, height, left, update: updateElementBounding } = useElementBounding(itemEl)
watch(top, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(left, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(height, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(() => props.category.active, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(selectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue) { nextTick(() => updateElementBounding()) }
})

const fontSize = computed(() => {
  return 1.0 + Math.min((props.category.rank-1)/8, 0.5)
})
const updateSelected = () => useResourceFilterStore().selectCategory(props.category.id)

const updateCoordinates = () => {
  if (top.value + height.value >= 0 && top.value <= window.innerHeight) {
    categoryCoordinateMap.value.set(props.category.id, {left: left.value - 5, y: top.value + (height.value/2)})
  } else {
    categoryCoordinateMap.value.delete(props.category.id)
  }
}
onMounted(() => {
  updateCoordinates()
})
onUnmounted(() => {
  categoryCoordinateMap.value.delete(props.category.id)
})
</script>

<template>
  <a ref="itemEl" v-motion-slide-visible-once-right
    class="nav-link ms-auto px-0 text-truncate" role="button"
    :class="{
      'active': category.active,
      'fw-bold': category.active,
      'text-decoration-underline': category.active,
      'text-light-emphasis': category.active,
      'text-light': !category.active,
    }"
    :style="{ 'font-size': `${fontSize}em` }"
    @click="updateSelected"
    :title="category.label"
  >{{ category.label }}</a>
</template>

<style scoped>
a {
  width: fit-content;
  max-width: 260px;
}
</style>