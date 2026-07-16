<script setup>
import { useTemplateRef, watch, onUnmounted, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore } from '../stores/resources.js'
import { useElementBounding } from '@vueuse/core'

const props = defineProps({
  resource: {
    type: Object,
    required: true,
  },
})

const resourceFilterStore = useResourceFilterStore()
const {
  selectedKey,
} = storeToRefs(resourceFilterStore)

const resourceCoordinateMap = defineModel('resourceCoordinateMap', { default: new Map() })

const itemEl = useTemplateRef('itemEl')
const { top, height, left, right, update: updateElementBounding } = useElementBounding(itemEl)
watch(top, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(height, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(left, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(right, (newValue, oldValue) => {
  if (newValue !== oldValue) { updateCoordinates() }
})
watch(selectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue) { nextTick(() => updateElementBounding()) }
})
const updateCoordinates = () => {
  if (top.value + height.value >= 0 && top.value <= window.innerHeight) {
    resourceCoordinateMap.value.set(props.resource.id, {left: left.value, right: right.value, y: top.value + (height.value/2)})
  } else {
    resourceCoordinateMap.value.delete(props.resource.id)
  }
}
onMounted(() => {
  updateCoordinates()
})
onUnmounted(() => {
  resourceCoordinateMap.value.delete(props.resource.id)
})
</script>

<template>
  <div ref="itemEl" class="card mb-5" v-motion-slide-visible-once-bottom>
    <img
      v-if="resource.images.length > 0 && resource.images[0].thumbnail"
      :src="resource.images[0].thumbnail" :alt="resource.images[0].name"
      class="card-img-top object-fit-cover w-100"
    >
    <div class="card-body">
      <a :href="`/resources/${resource.id}`"
        class="link-offset-2 link-underline link-light link-underline-opacity-50 link-underline-opacity-100-hover icon-link icon-link-hover"
      >
        {{ resource.name }}
        <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16" aria-hidden="true">
          <path d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
        </svg>
      </a>
    </div>
  </div>
</template>

<style scoped>
  img {
    max-height: 250px;
  }
</style>