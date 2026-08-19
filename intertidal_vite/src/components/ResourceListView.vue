<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { breakpointsBootstrapV5, useBreakpoints } from '@vueuse/core'
import { useResourcesFilterStore } from '../stores/display.js'
import { useResourcesStore, usePeopleStore, useOrganizationsStore } from '../stores/data.js'
import ContributorFilterListItem from './ContributorFilterListItem.vue'
import { CategoryTypes, LocaleTypes } from '../_resourceTypes.js'
import ResourceListItem from './ResourceListItem.vue'
import CategoryFilterListItem from './CategoryFilterListItem.vue'
import ConnectionsCanvas from './ConnectionsCanvas.vue'

const breakpoints = useBreakpoints(breakpointsBootstrapV5)
const isLargeScreen = breakpoints.greaterOrEqual('xl')

 // filter all ROUNDTABLE_INTERVIEW (Roundtable/Interview). It is displayed elsewhere
const resources = (await useResourcesStore().getAll()).filter((o) => !o.categories.includes('ROUNDTABLE_INTERVIEW')).map((o) => ({...o, key: `resource_${o.id}` }))
const categorySet = resources.reduce((result, o) => result = result.union(new Set(o.categories)), new Set())
const categories = Array.from(categorySet)
  .sort((a, b) => `${a}`.localeCompare(b))
  .map((o) => ({label: CategoryTypes[o], id: o, key: `category_${o}`}))
const people = (await usePeopleStore().getAll()).map((o) => ({...o, key: `person_${o.id}`}))
const organizations = (await useOrganizationsStore().getAll()).map((o) => ({...o, key: `organization_${o.id}`}))

const {
  objectMap: resourceObjectMap,
} = storeToRefs(useResourcesStore())
const {
  objectMap: personObjectMap,
} = storeToRefs(usePeopleStore())
const {
  objectMap: organizationObjectMap,
} = storeToRefs(useOrganizationsStore())
const {
  selectedKey,
  selectedType,
  selectedValue,
} = storeToRefs(useResourcesFilterStore())

const dropdownContributorSelectedKey = ref(null)
watch(dropdownContributorSelectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue && newValue && selectedKey.value !== newValue) {
    const organizationPrefix = 'organization_'
    const personPrefix = 'person_'
    if (newValue.startsWith(organizationPrefix)) {
      useResourcesFilterStore().selectOrganization(parseInt(newValue.slice(organizationPrefix.length)))
    } else if (newValue.startsWith(personPrefix)) {
      useResourcesFilterStore().selectPerson(parseInt(newValue.slice(personPrefix.length)))
    }
  }
})
const dropdownCategorySelectedKey = ref(null)
watch(dropdownCategorySelectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue && newValue && selectedKey.value !== newValue) {
    const categoryPrefix = 'category_'
    if (newValue.startsWith(categoryPrefix)) {
      useResourcesFilterStore().selectCategory(newValue.slice(categoryPrefix.length))
    }
  }
})
const resetDropdownFilters = () => {
  if (selectedValue.value) {
    if (['organization', 'person'].includes(selectedType.value) ) {
      dropdownContributorSelectedKey.value = selectedKey.value
      dropdownCategorySelectedKey.value = null
    } else if (selectedType.value === 'category') {
      dropdownContributorSelectedKey.value = null
      dropdownCategorySelectedKey.value = selectedKey.value
    }
  } else {
    dropdownContributorSelectedKey.value = null
    dropdownCategorySelectedKey.value = null
  }
}
const dropdownClearSelected = () => {
  useResourcesFilterStore().$reset()
  dropdownContributorSelectedKey.value = null
  dropdownCategorySelectedKey.value = null
}

const resourcesHeaderRef = ref(null)

const scrollToTopOfResources = () => resourcesHeaderRef.value?.scrollIntoView({ behavior: 'instant', block: 'start' })
watch(selectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (newValue) { nextTick(scrollToTopOfResources) }
    resetDropdownFilters()
  }
})

const entityHoverKey = ref(null)
const filteredResources = computed(() => resources.filter((o) => {
  if (selectedType.value === 'person' && !o.person_ids.includes(selectedValue.value)) { return false }
  if (selectedType.value === 'organization' && !o.organization_ids.includes(selectedValue.value)) { return false }
  if (selectedType.value === 'locale' && o.locale !== selectedValue.value) { return false }
  if (selectedType.value === 'category' && !o.categories.includes(selectedValue.value)) { return false }
  return true
}))
const resourceCoordinateMap = ref(new Map())
const visibleResourceIds = computed(() => Array.from(resourceCoordinateMap.value.keys()))

const collaboratorCoordinateMap = ref(new Map())
const rankedCollaboratorMap = computed(() => {
  const references = new Map()
  visibleResourceIds.value.forEach( (resource_id) => {
    const resource = resourceObjectMap.value.get(resource_id)
    if (resource) {
      resource.person_ids.forEach((id) => references.set(`person_${id}`, (references.get(`person_${id}`) ?? 0) + 1 ))
      resource.organization_ids.forEach((id) => references.set(`organization_${id}`, (references.get(`organization_${id}`) ?? 0) + 1 ))
    }
  })
  return [...references.entries()]
    .filter((a) => a[1] > 0)
    .sort((a, b) => {
      // prioritize selected in case everything has equal references
      if (a[0] === selectedKey.value) { return -1 } else if (b[0] === selectedKey.value) { return 1 }
      return a[1] - b[1]
    })
    .slice(0, 15)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const contributorList = computed(() =>
  [
    ...people.filter((o) => rankedCollaboratorMap.value.has(`person_${o.id}`)).map((o) => ({...o, rank: rankedCollaboratorMap.value.get(`person_${o.id}`), active: selectedKey.value === `person_${o.id}`})),
    ...organizations.filter((o) => rankedCollaboratorMap.value.has(`organization_${o.id}`)).map((o) => ({...o, rank: rankedCollaboratorMap.value.get(`organization_${o.id}`), active: selectedKey.value === `organization_${o.id}`}))
  ].sort((a, b) => `${a.label}`.localeCompare(b.label))
)
const collaboratorReferencesMap = computed(() => {
  const references = new Map()
  resources.forEach( (resource) => {
    resource.person_ids.forEach((id) => references.set(`person_${id}`, (references.get(`person_${id}`) ?? 0) + 1 ))
    resource.organization_ids.forEach((id) => references.set(`organization_${id}`, (references.get(`organization_${id}`) ?? 0) + 1 ))
  })
  return [...references.entries()]
    .filter((a) => a[1] > 0)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const dropdownContributorList = computed(() =>
  [
    ...people.filter((o) => collaboratorReferencesMap.value.has(`person_${o.id}`)),
    ...organizations.filter((o) => collaboratorReferencesMap.value.has(`organization_${o.id}`))
  ].sort((a, b) => `${a.label}`.localeCompare(b.label))
)

const categoryCoordinateMap = ref(new Map())
const rankedCategoryMap = computed(() => {
  const references = new Map()
  visibleResourceIds.value.forEach( (resource_id) => {
    const resource = resourceObjectMap.value.get(resource_id)
    if (resource) {
      resource.categories.forEach((category) => references.set(category, (references.get(category) ?? 0) + 1 ))
    }
  })
  return [...references.entries()]
    .filter((a) => a[1] > 0)
    .sort((a, b) => {
      // prioritize selected in case everything has equal references
      if (`category_${a[0]}` === selectedKey.value) { return -1 } else if (`category_${b[0]}` === selectedKey.value) { return 1 }
      return a[1] - b[1]
    })
    .slice(0, 15)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const categoryList = computed(() => categories.filter((o) => rankedCategoryMap.value.has(o.id)).map((o) => ({...o, rank: rankedCategoryMap.value.get(o.id), active: selectedKey.value === `category_${o.id}`})))
const categoryReferenceMap = computed(() => {
  const references = new Map()
  resources.forEach( (resource) => {
    resource.categories.forEach((category) => references.set(category, (references.get(category) ?? 0) + 1 ))
  })
  return [...references.entries()]
    .filter((a) => a[1] > 0)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const dropdownCategoryList = computed(() => categories.filter(({id}) => categoryReferenceMap.value.has(id)))
onMounted(() => {
  resetDropdownFilters()
})
</script>

<template>
  <div class="position-relative">
    <ConnectionsCanvas class="z-1"
      v-if="isLargeScreen"
      v-model:entityHoverKey="entityHoverKey"
      v-model:resourceCoordinateMap="resourceCoordinateMap"
      v-model:collaboratorCoordinateMap="collaboratorCoordinateMap"
      v-model:categoryCoordinateMap="categoryCoordinateMap"
    />
    <div class="app-resource-viz-wrapper position-relative z-2 d-flex w-100 px-3">
      <div class="sticky-top py-3 h-100 text-start contributor-filter-wrapper" v-if="isLargeScreen">
        <h2 class="h2">Contributors</h2>
        <ul class="nav flex-column">
          <ContributorFilterListItem v-for="contributor in contributorList" :key="contributor.key"
            :contributor="contributor" v-model:collaboratorCoordinateMap="collaboratorCoordinateMap"
            @mouseenter="() => entityHoverKey = contributor.key"
            @mouseleave="() => entityHoverKey = null"
          />
        </ul>
      </div>
      <div class="px-0 h-100 flex-grow-1 resource-list-wrapper"
        :class="{ 'w-100': !isLargeScreen, 'mx-5': isLargeScreen }"
      >
        <h2 ref="resourcesHeaderRef" class="resource-heading h4 text-center">
          <span v-if="selectedType === 'locale'">
            <span class="btn-link fw-bold" @click="useResourcesFilterStore().$reset()">{{ LocaleTypes[selectedValue] }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'category'">
            <span class="btn-link fw-bold text-capitalize" @click="useResourcesFilterStore().$reset()">{{ CategoryTypes[selectedValue] }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'person'">
            <span class="btn-link fw-bold" @click="useResourcesFilterStore().$reset()">{{ personObjectMap.get(selectedValue).label }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'organization'">
            <span class="btn-link fw-bold" @click="useResourcesFilterStore().$reset()">{{ organizationObjectMap.get(selectedValue).label }}</span>
            Resources
          </span>
          <span v-if="!selectedType">All Resources</span>
        </h2>
        <div class="d-flex mt-3" v-if="!isLargeScreen">
          <Multiselect
            v-model="dropdownContributorSelectedKey"
            :options="dropdownContributorList.map((o) => o.key)" :custom-label="(key) => dropdownContributorList.find((o) => o.key === key)?.label"
            :close-on-select="true" placeholder="Select a Contributor" :show-labels="false"
            class="me-2"
          >
            <template #clear="props">
              <i class="bi bi-x-lg fw-bold fs-6 multiselect__clear" title="Clear" v-if="dropdownContributorSelectedKey" @mousedown.prevent.stop="dropdownClearSelected()"></i>
            </template>
          </Multiselect>
          <Multiselect
            v-model="dropdownCategorySelectedKey"
            :options="dropdownCategoryList.map((o) => o.key)" :custom-label="(key) => dropdownCategoryList.find((o) => o.key === key)?.label"
            :close-on-select="true" placeholder="Select a Category" :show-labels="false"
            class="ms-2"
          >
            <template #clear="props">
              <i class="bi bi-x-lg fw-bold fs-6 multiselect__clear" title="Clear" v-if="dropdownCategorySelectedKey" @mousedown.prevent.stop="dropdownClearSelected()"></i>
            </template>
          </Multiselect>
        </div>
        <hr />
        <ResourceListItem v-for="resource in filteredResources" :key="resource.id"
          :resource="resource" v-model:resourceCoordinateMap="resourceCoordinateMap"
          @mouseenter="() => entityHoverKey = resource.key"
          @mouseleave="() => entityHoverKey = null"
        />
      </div>
      <div class="sticky-top py-3 h-100 text-end category-filter-wrapper" v-if="isLargeScreen">
        <h2 class="h2">Categories</h2>
        <ul class="nav flex-column">
          <CategoryFilterListItem v-for="category in categoryList" :key="category.key"
            :category="category" v-model:categoryCoordinateMap="categoryCoordinateMap"
            @mouseenter="() => entityHoverKey = category.key"
            @mouseleave="() => entityHoverKey = null"
           />
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-resource-viz-wrapper {
  min-height: calc(100vh - 3rem - 105px) !important;
}
.resource-heading {
  span.btn-link {
    cursor: pointer;
  }
}
.contributor-filter-wrapper,
.category-filter-wrapper {
  width: 300px !important;
}
</style>