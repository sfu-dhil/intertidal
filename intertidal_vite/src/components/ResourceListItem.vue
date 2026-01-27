<script setup>
import { useTemplateRef, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore, useResourceGraphStore } from '../stores/resources.js'
import { LocaleTypes } from '../helpers/localeTypes.js'
import { CategoryTypes } from '../helpers/categoryTypes.js'
import { ClsTypes } from '../helpers/clsTypes.js'
import { useElementVisibility } from '@vueuse/core'


const resourceFilterStore = useResourceFilterStore()
const {
  filteredResourceIdSet,
} = storeToRefs(resourceFilterStore)

const props = defineProps({
  resource: {
    type: Object,
    required: true,
  },
})


const itemEl = useTemplateRef('itemEl')
const itemElVisible = useElementVisibility(itemEl, {
  threshold: 0.1,
})

const displayResourceClasses = computed(() => filteredResourceIdSet.value.has(props.resource.id) ? '' : 'd-none')
const languageNames = new Intl.DisplayNames(["en"], { type: "language" })

watch(itemElVisible, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    useResourceGraphStore().updateResourceVisible(props.resource.id, newValue)
  }
})
</script>

<template>
  <div ref="itemEl"
    class="card d-flex flex-row align-items-center my-3 p-3 position-relative"
    :class="displayResourceClasses"
  >
    <img
      v-if="resource.images.length > 0 && resource.images[0].thumbnail"
      :src="resource.images[0].thumbnail" :alt="resource.images[0].name"
      class="img-fluid rounded flex-shrink-0"
    >
    <div class="card-body flex-grow-1 py-0">
      <h5 class="mt-0">{{ resource.name }}</h5>
      <div class="mb-3">
        <span v-if="resource.locale" class="badge text-bg-primary me-1" :title="`Locale: ${LocaleTypes[resource.locale]}`">{{ LocaleTypes[resource.locale] }}</span>
        <span v-if="resource.language" class="badge text-bg-primary me-1" :title="`Language: ${languageNames.of(resource.language)}`">{{ languageNames.of(resource.language) }}</span>
        <span v-for="category in resource.categories" class="badge text-bg-primary me-1" :title="`Category: ${CategoryTypes[category]}`">{{ CategoryTypes[category] }}</span>
        <span v-for="form in resource.forms" class="badge text-bg-primary me-1" :title="`Physical/Digital Form: ${ClsTypes[form]}`">{{ ClsTypes[form] }}</span>
      </div>
    </div>
    <a :href="`/resources/${resource.id}`" class="btn btn-primary stretched-link">View <i class="bi bi-box-arrow-up-right"></i></a>
  </div>
</template>

<style scoped>
  card {
    cursor: pointer;
  }
  img {
    max-width: 100px;
    object-fit: contain;
  }
</style>