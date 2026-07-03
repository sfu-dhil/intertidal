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
  contributor: {
    type: Object,
    required: true,
  },
})
const collaboratorCoordinateMap = defineModel('collaboratorCoordinateMap', { default: new Map() })


const itemEl = useTemplateRef('itemEl')
const { top, height, right, update: updateElementBounding } = useElementBounding(itemEl)
watch(top, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(right, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(height, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(selectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue) { nextTick(() => updateElementBounding()) }
})

const fontSize = computed(() => {
  return 1.0 + Math.min((props.contributor.rank-1)/8, 0.5)
})
const updateSelected = () => props.contributor.key.startsWith('person_') ? useResourceFilterStore().selectPerson(props.contributor.id) : useResourceFilterStore().selectOrganization(props.contributor.id)

const updateCoordinates = () => {
  if (top.value + height.value >= 0 && top.value <= window.innerHeight) {
    collaboratorCoordinateMap.value.set(props.contributor.key, {right: right.value + 5, y: top.value + (height.value/2)})
  } else {
    collaboratorCoordinateMap.value.delete(props.contributor.key)
  }
}
onMounted(() => {
  updateCoordinates()
})
onUnmounted(() => {
  collaboratorCoordinateMap.value.delete(props.contributor.key)
})
</script>

<template>
  <a ref="itemEl" v-motion-slide-visible-once-left
    class="nav-link me-auto px-0 text-truncate" role="button"
    :class="{
      'active': contributor.active,
      'fw-bold': contributor.active,
      'text-decoration-underline': contributor.active,
      'text-light-emphasis': contributor.active,
      'text-light': !contributor.active,
    }"
    :style="{ 'font-size': `${fontSize}em` }"
    @click="updateSelected"
    :title="contributor.label"
  >{{ contributor.label }}</a>
</template>

<style scoped>
a {
  width: fit-content;
  max-width: 260px;
}
</style>