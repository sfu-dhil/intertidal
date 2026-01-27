<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore, useResourceGraphStore } from '../stores/resources.js'

const resourceFilterStore = useResourceFilterStore()
const {
  selectedPersonId,
  selectedOrganizationId,
} = storeToRefs(resourceFilterStore)
const resourceGraphStore = useResourceGraphStore()
const {
  rankedCollaborationMap,
} = storeToRefs(resourceGraphStore)

const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
})


const isPerson = computed(() => props.type === 'person')
const isOrganization = computed(() => props.type === 'organization')
const isActive = computed(() => (isPerson.value && selectedPersonId.value === props.id) || (isOrganization.value && selectedOrganizationId.value === props.id) )
const activeClass = computed(() => isActive.value ? 'active fw-bold text-light-emphasis fs-5' : 'text-light fs-6')
const isDisplayedClass = computed(() => isActive.value || rankedCollaborationMap.value.has(`${props.type}_${props.id}`) ? '' : 'd-none' )
const updateSelected = () => isPerson.value ? useResourceFilterStore().updateSelectedPerson(props.id) : useResourceFilterStore().updateSelectedOrganization(props.id)
</script>

<template>
  <li class="nav-item" :class="isDisplayedClass">
    <a class="nav-link bg-transparent d-inline-block text-truncate" :class="activeClass"
      @click="updateSelected"
      :title="label"
      role="button"
    >{{ label }}</a>
  </li>
</template>

<style scoped>
  .nav-link {
    width: 250px;
  }
</style>