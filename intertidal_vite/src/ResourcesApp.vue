<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceStore } from './stores/resources.js'
import ContributorFilterList from './components/ContributorFilterList.vue'
import ResourceList from './components/ResourceList.vue'
import KeywordFilterList from './components/KeywordFilterList.vue'

const props = defineProps({
  resources: {
    type: Array,
  },
  people: {
    type: Array,
  },
  organizations: {
    type: Array,
  },
})

const resourceDataStore = useResourceStore()
const {
  resources,
} = storeToRefs(resourceDataStore)


// setup init data
resourceDataStore.initData(props.resources, props.people, props.organizations)

</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="sticky-top p-3 pe-5 h-100">
      <h2 class="h4 text-center">Contributors</h2>
      <hr />
      <ContributorFilterList />
    </div>
    <div class="container flex-grow-1 mx-0 px-0 h-100">
      <h2 class="h4 text-center">Resources</h2>
      <ResourceList />
    </div>
    <div class="sticky-top p-3 pe-5 h-100">
      <h2 class="h4 text-center">Keywords</h2>
      <hr />
      <KeywordFilterList />
    </div>
  </div>
</template>

<style scoped>
</style>