<script setup>
import { useTemplateRef, watch, onUnmounted, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore } from '../stores/resources.js'
import { LocaleTypes } from '../helpers/localeTypes.js'
import { CategoryTypes } from '../helpers/categoryTypes.js'
import { ClsTypes } from '../helpers/clsTypes.js'
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
// const resourceDataStore = useResourceStore()
// const {
//   personMap,
//   marcRelatorsMap,
// } = storeToRefs(resourceDataStore)
// const languageNames = new Intl.DisplayNames(["en"], { type: "language" })
// const dateRange = computed(() => {
//   const dateParts = []
//   if (props.resource.date) { dateParts.push(props.resource.date) }
//   if (props.resource.date_current) { dateParts.push('Current') }
//   if (!props.resource.date_current && props.resource.date_end) { dateParts.push(props.resource.date_end) }
//   return dateParts.join(' - ')
// })

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
<!--
    <span v-if="resource.locale" class="badge text-bg-primary me-1" :title="`Locale: ${LocaleTypes[resource.locale]}`">{{ LocaleTypes[resource.locale] }}</span>
    <span v-if="resource.language" class="badge text-bg-primary me-1" :title="`Language: ${languageNames.of(resource.language)}`">{{ languageNames.of(resource.language) }}</span>
    <span v-for="category in resource.categories" class="badge text-bg-primary me-1" :title="`Category: ${CategoryTypes[category]}`">{{ CategoryTypes[category] }}</span>
    <span v-for="form in resource.forms" class="badge text-bg-primary me-1" :title="`Physical/Digital Form: ${ClsTypes[form]}`">{{ ClsTypes[form] }}</span>
    <br /> {{ dateRange }}
    <br /> -->
    <!-- <span v-for="(statement, statementIndex) in resource.person_responsibility_statements">
      <a href="javascript:void(0)"
        class="link-offset-2 link-underline link-light link-underline-opacity-50 link-underline-opacity-100-hover"
      >{{ personMap.get(statement.person).label }}</a>&nbsp;
      <span
        v-for="(marc_relator, index) in statement.marc_relators" class="badge text-bg-primary"
        :class="{'ms-1': index > 0}"
        :title="`Role: ${marcRelatorsMap.get(marc_relator)}`"
      >{{ marcRelatorsMap.get(marc_relator) }}</span>{{ statementIndex < resource.person_responsibility_statements.length - 1 ? ', ' : '' }}
    </span> -->
  </div>
</template>

<style scoped>
  img {
    max-height: 250px;
  }
</style>