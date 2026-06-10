import { defineStore } from 'pinia'

export const useResourceStore = defineStore('resources-data', {
  state: () => ({
    resources: [],
    people: [],
    organizations: [],
    marcRelatorsMap: new Map(),
  }),
  getters: {
    resourceMap: (state) => state.resources.reduce((result, o) => result.set(o.id, o), new Map()),
    personMap: (state) => state.people.reduce((result, o) => result.set(o.id, o), new Map()),
    organizationMap: (state) => state.organizations.reduce((result, o) => result.set(o.id, o), new Map()),
    keywordSet: (state) => state.resources.reduce((result, o) => result = result.union(o.keyword_set), new Set()),
    keywords: (state) => Array.from(state.keywordSet).sort((a, b) => `${a}`.localeCompare(b)),
    localeSet: (state) => new Set(state.resources.map((o) => o.locale)),
    locales: (state) => Array.from(state.localeSet).sort((a, b) => `${a.label}`.localeCompare(b.label)),
    categorySet: (state) => state.resources.reduce((result, o) => result = result.union(o.category_set), new Set()),
    categories: (state) => Array.from(state.categorySet).sort((a, b) => `${a}`.localeCompare(b)),
  },
  actions: {
    initData(resources, people, organizations, marcRelators) {
      // transform/simplify resource data for easier filtering
      resources.forEach(resource => {
        resource.key = `resource_${resource.id}`
        resource.category_set = new Set(resource.categories)
        resource.keyword_set = new Set(resource.keywords)
        resource.person_id_set = new Set(resource.person_ids)
        resource.organization_id_set = new Set(resource.organization_ids)
        resource.form_set = new Set(resource.forms)
      })

      this.resources = resources
      this.people = people
      this.organizations = organizations
      this.marcRelatorsMap = marcRelators.reduce((result, {0: value, 1: label}) => result.set(value, label), new Map())
    },
    getResource(id) {
      return this.resourceMap.has(id) ? this.resourceMap.get(id) : null
    },
    getPerson(id) {
      return this.personMap.has(id) ? this.personMap.get(id) : null
    },
    getOrganization(id) {
      return this.organizationMap.has(id) ? this.organizationMap.get(id) : null
    },
  },
  persist: false,
})

export const useResourceFilterStore = defineStore('resources-filter', {
  state: () => ({
    selectedType: null,
    selectedValue: null,
  }),
  getters: {
    selectedKey: (state) => state.selectedType && state.selectedValue ? `${state.selectedType}_${state.selectedValue}` : null,
  },
  actions: {
    reset() {
      this.selectedType = null
      this.selectedValue = null
    },
    selectPerson(personId) {
      if (this.selectedType === 'person' && this.selectedValue === personId) {
        this.reset()
      } else {
        this.selectedType = 'person'
        this.selectedValue = personId
      }
    },
    selectOrganization(organizationId) {
      if (this.selectedType === 'organization' && this.selectedValue === organizationId) {
        this.reset()
      } else {
        this.selectedType = 'organization'
        this.selectedValue = organizationId
      }
    },
    selectLocale(locale) {
      if (this.selectedType === 'locale' && this.selectedValue === locale) {
        this.reset()
      } else {
        this.selectedType = 'locale'
        this.selectedValue = locale
      }
    },
    selectCategory(category) {
      if (this.selectedType === 'category' && this.selectedValue === category) {
        this.reset()
      } else {
        this.selectedType = 'category'
        this.selectedValue = category
      }
    },
  },
  persist: true,
})