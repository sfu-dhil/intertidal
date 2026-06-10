<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore, useResourceStore } from './stores/resources.js'
import ContributorFilterListItem from './components/ContributorFilterListItem.vue'
import { LocaleTypes } from './helpers/localeTypes.js'
import { CategoryTypes } from './helpers/categoryTypes.js'
import ResourceListItem from './components/ResourceListItem.vue'
import CategoryFilterListItem from './components/CategoryFilterListItem.vue'
import ConnectionsCanvas from './components/ConnectionsCanvas.vue'

const props = defineProps({
  resources: {
    type: Array,
    required: true,
  },
  people: {
    type: Array,
    required: true,
  },
  organizations: {
    type: Array,
    required: true,
  },
  marcRelators: {
    type: Array,
    required: true,
  },
})

const resourceDataStore = useResourceStore()
// setup init data
resourceDataStore.initData(props.resources, props.people, props.organizations, props.marcRelators)
const {
  resources,
  people,
  personMap,
  organizations,
  organizationMap,
  // locales,
  categories,
} = storeToRefs(resourceDataStore)
const resourceFilterStore = useResourceFilterStore()
const {
  selectedKey,
  selectedType,
  selectedValue,
} = storeToRefs(resourceFilterStore)

const resourcesHeaderRef = ref(null)

const scrollToTopOfResources = () => resourcesHeaderRef.value?.scrollIntoView({ behavior: 'instant', block: 'start' })
watch(selectedKey, (newValue) => {
  if (newValue) { nextTick(scrollToTopOfResources) }
})

const entityHoverKey = ref(null)
const filteredResources = computed(() => resources.value.filter((o) => {
  if (selectedType.value === 'person' && !o.person_id_set.has(selectedValue.value)) { return false }
  if (selectedType.value === 'organization' && !o.organization_id_set.has(selectedValue.value)) { return false }
  if (selectedType.value === 'locale' && o.locale !== selectedValue.value) { return false }
  if (selectedType.value === 'category' && !o.category_set.has(selectedValue.value)) { return false }
  return true
}))
const resourceCoordinateMap = ref(new Map())
const visibleResourceIds = computed(() => Array.from(resourceCoordinateMap.value.keys()))

const collaboratorCoordinateMap = ref(new Map())
const rankedCollaboratorMap = computed(() => {
  const collaboratorReferences = new Map()
  visibleResourceIds.value.forEach( (resource_id) => {
    const resource = useResourceStore().resourceMap.get(resource_id)
    if (resource) {
      resource.person_ids.forEach((id) => collaboratorReferences.set(`person_${id}`, (collaboratorReferences.get(`person_${id}`) ?? 0) + 1 ))
      resource.organization_ids.forEach((id) => collaboratorReferences.set(`organization_${id}`, (collaboratorReferences.get(`organization_${id}`) ?? 0) + 1 ))
    }
  })
  return [...collaboratorReferences.entries()]
    .filter((a) => a[1] > 0)
    .sort((a, b) => {
      // prioritize selected in case everything has equal references
      if (a[0] === selectedKey.value) {
        return -1
      } else if (b[0] === selectedKey.value) {
        return 1
      }
      return a[1] - b[1]
    })
    .slice(0, 15)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const contributorList = computed(() =>
  [
    ...people.value.filter((o) => rankedCollaboratorMap.value.has(`person_${o.id}`)).map((o) => ({...o, key: `person_${o.id}`, rank: rankedCollaboratorMap.value.get(`person_${o.id}`), active: selectedKey.value === `person_${o.id}`})),
    ...organizations.value.filter((o) => rankedCollaboratorMap.value.has(`organization_${o.id}`)).map((o) => ({...o, key: `organization_${o.id}`, rank: rankedCollaboratorMap.value.get(`organization_${o.id}`), active: selectedKey.value === `organization_${o.id}`}))
  ].sort((a, b) => `${a.label}`.localeCompare(b.label))
)

const categoryCoordinateMap = ref(new Map())
const rankedCategoryMap = computed(() => {
  const category_references = new Map()
  visibleResourceIds.value.forEach( (resource_id) => {
    const resource = useResourceStore().resourceMap.get(resource_id)
    if (resource) {
      resource.categories.forEach((category) => category_references.set(category, (category_references.get(category) ?? 0) + 1 ))
    }
  })
  return [...category_references.entries()]
    .filter((a) => a[1] > 0)
    .sort((a, b) => {
      // prioritize selected in case everything has equal references
      if (`category_${a[0]}` === selectedKey.value) {
        return -1
      } else if (`category_${b[0]}` === selectedKey.value) {
        return 1
      }
      return a[1] - b[1]
    })
    .slice(0, 15)
    .reduce((result, a) => result.set(a[0], a[1]), new Map())
})
const categoryList = computed(() => categories.value.filter((category) => rankedCategoryMap.value.has(category)).map((category) => ({label: CategoryTypes[category], id: category, key: `category_${category}`, rank: rankedCategoryMap.value.get(category), active: selectedKey.value === `category_${category}`})))
</script>

<template>
  <div class="position-relative">
    <ConnectionsCanvas class="z-1"
      v-model:entityHoverKey="entityHoverKey"
      v-model:resourceCoordinateMap="resourceCoordinateMap"
      v-model:collaboratorCoordinateMap="collaboratorCoordinateMap"
      v-model:categoryCoordinateMap="categoryCoordinateMap"
    />
    <div class="app-resource-viz-wrapper position-relative z-2 d-flex justify-content-center">
      <div class="sticky-top py-3 px-5 ms-5 h-100 text-start contributor-filter-wrapper">
        <h2 class="h2">Contributors</h2>
        <nav class="nav flex-column nav-filter-list">
          <ContributorFilterListItem v-for="contributor in contributorList" :key="contributor.key"
            :contributor="contributor" v-model:collaboratorCoordinateMap="collaboratorCoordinateMap"
            @mouseenter="() => entityHoverKey = contributor.key"
            @mouseleave="() => entityHoverKey = null"
          />
        </nav>
      </div>
      <div class="mx-5 px-0 h-100 resource-list-wrapper">
        <h2 ref="resourcesHeaderRef" class="resource-heading h4 text-center">
          <span v-if="selectedType === 'locale'">
            <span class="btn-link fw-bold" @click="useResourceFilterStore().reset()">{{ LocaleTypes[selectedValue] }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'category'">
            <span class="btn-link fw-bold text-capitalize" @click="useResourceFilterStore().reset()">{{ CategoryTypes[selectedValue] }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'person'">
            <span class="btn-link fw-bold" @click="useResourceFilterStore().reset()">{{ personMap.get(selectedValue).label }}</span>
            Resources
          </span>
          <span v-if="selectedType === 'organization'">
            <span class="btn-link fw-bold" @click="useResourceFilterStore().reset()">{{ organizationMap.get(selectedValue).label }}</span>
            Resources
          </span>
          <span v-if="!selectedType">All Resources</span>
        </h2>
        <hr />
        <ResourceListItem v-for="resource in filteredResources" :key="resource.id"
          :resource="resource" v-model:resourceCoordinateMap="resourceCoordinateMap"
          @mouseenter="() => entityHoverKey = resource.key"
          @mouseleave="() => entityHoverKey = null"
        />
      </div>
      <div class="sticky-top py-3 px-5 me-5 h-100 text-end category-filter-wrapper">
        <h2 class="h2">Categories</h2>
        <nav class="nav flex-column nav-filter-list">
          <CategoryFilterListItem v-for="category in categoryList" :key="category.key"
            :category="category" v-model:categoryCoordinateMap="categoryCoordinateMap"
            @mouseenter="() => entityHoverKey = category.key"
            @mouseleave="() => entityHoverKey = null"
           />
        </nav>
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
  width: 400px !important;
}
.resource-list-wrapper {
  width: 800px !important;
}
</style>