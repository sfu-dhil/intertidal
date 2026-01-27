import { defineStore } from 'pinia'

export const useResourceStore = defineStore('resources-data', {
  state: () => ({
    resources: [],
    people: [],
    organizations: [],
  }),
  getters: {
    resourceMap: (state) => state.resources.reduce((result, o) => result.set(o.id, o), new Map()),
    personMap: (state) => state.people.reduce((result, o) => result.set(o.id, o), new Map()),
    organizationMap: (state) => state.organizations.reduce((result, o) => result.set(o.id, o), new Map()),
    keywordSet: (state) => state.resources.reduce((result, o) => result = result.union(o.keyword_set), new Set()),
    keywords: (state) => Array.from(state.keywordSet).sort((a, b) => `${a.label}`.localeCompare(b.label)),
  },
  actions: {
    initData(resources, people, organizations) {
      // transform/simplify resource data for easier filtering
      resources.forEach(resource => {
        resource.category_set = new Set(resource.categories)
        resource.keyword_set = new Set(resource.keywords)
        resource.person_id_set = new Set(resource.person_ids)
        resource.organization_id_set = new Set(resource.organization_ids)
        resource.form_set = new Set(resource.forms)
      })

      this.resources = resources
      this.people = people
      this.organizations = organizations
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
    selectedPersonId: null,
    selectedOrganizationId: null,
    selectedLocale: null,
    selectedCategory: null,
    selectedKeyword: null,
  }),
  getters: {
    filteredResourceIdSet: (state) => useResourceStore().resources.filter((o) => {
      if(state.selectedPersonId && !o.person_id_set.has(state.selectedPersonId)) { return false }
      if(state.selectedOrganizationId && !o.organization_id_set.has(state.selectedOrganizationId)) { return false }
      if(state.selectedKeyword && !o.keyword_set.has(state.selectedKeyword)) { return false }
      return true
    }).reduce((result, o) => result.add(o.id), new Set()),
  },
  actions: {
    updateSelectedPerson(person_id) {
      this.selectedPersonId = this.selectedPersonId === person_id ? null : person_id
      this.selectedOrganizationId = null
    },
    updateSelectedOrganization(organization_id) {
      this.selectedPersonId = null
      this.selectedOrganizationId = this.selectedOrganizationId === organization_id ? null : organization_id
    },
    updateSelectedKeyword(keyword) {
      this.selectedKeyword = this.selectedKeyword === keyword ? null : keyword
    }
  },
  persist: true,
})

export const useResourceGraphStore = defineStore('resources-graph', {
  state: () => ({
    visibleResourceIds: [],
  }),
  getters: {
    visibleResourceIdSet: (state) => new Set(state.visibleResourceIds),
    rankedCollaborationMap: (state) => {
      const collaboration_references = new Map()
      state.visibleResourceIds.forEach( (resource_id) => {
        const resource = useResourceStore().resourceMap.get(resource_id)
        if (resource) {
          resource.person_ids.forEach((id) => collaboration_references.set(`person_${id}`, (collaboration_references.get(`person_${id}`) ?? 0) + 1 ))
          resource.organization_ids.forEach((id) => collaboration_references.set(`organization_${id}`, (collaboration_references.get(`organization_${id}`) ?? 0) + 1 ))
        }
      })
      return [...collaboration_references.entries()].sort((a, b) => {
        // prioritize selected in case everything has equal references
        if ([`person_${useResourceFilterStore().selectedPersonId}`, `organization_${useResourceFilterStore().selectedOrganizationId}`].includes(a[0])) {
          return -1
        } else if ([`person_${useResourceFilterStore().selectedPersonId}`, `organization_${useResourceFilterStore().selectedOrganizationId}`].includes(b[0])) {
          return 1
        }
        return a[1] - b[1]
      }).slice(0, 10).reduce((result, a) => result.set(a[0], a[1]), new Map())
    },
    rankedKeywordMap: (state) => {
      const keyword_references = new Map()
      state.visibleResourceIds.forEach( (resource_id) => {
        const resource = useResourceStore().resourceMap.get(resource_id)
        if (resource) {
          resource.keywords.forEach((keyword) => keyword_references.set(keyword, (keyword_references.get(keyword) ?? 0) + 1 ))
        }
      })
      return [...keyword_references.entries()].sort((a, b) => {
        // prioritize selected in case everything has equal references
        if (a[0] === useResourceFilterStore().selectedKeyword) {
          return -1
        } else if (b[0] === useResourceFilterStore().selectedKeyword) {
          return 1
        }
        return a[1] - b[1]
      }).slice(0, 10).reduce((result, a) => result.set(a[0], a[1]), new Map())
    },
  },
  actions: {
    updateResourceVisible(resource_id, visible) {
      this.visibleResourceIds = Array.from(visible ? this.visibleResourceIdSet.union(new Set([resource_id])) : this.visibleResourceIdSet.difference(new Set([resource_id])))
    },
  },
  persist: false,
})