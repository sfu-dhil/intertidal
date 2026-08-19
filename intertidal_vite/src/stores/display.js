import { defineStore } from 'pinia'

export const useResourcesFilterStore = defineStore('display-resources-filter', {
  state: () => ({
    selectedType: null,
    selectedValue: null,
  }),
  getters: {
    selectedKey: (state) => state.selectedType && state.selectedValue ? `${state.selectedType}_${state.selectedValue}` : null,
  },
  actions: {
    reset() {
      this.$reset()
    },
    selectPerson(personId) {
      if (this.selectedType === 'person' && this.selectedValue === personId) {
        this.$reset()
      } else {
        this.selectedType = 'person'
        this.selectedValue = personId
      }
    },
    selectOrganization(organizationId) {
      if (this.selectedType === 'organization' && this.selectedValue === organizationId) {
        this.$reset()
      } else {
        this.selectedType = 'organization'
        this.selectedValue = organizationId
      }
    },
    selectLocale(locale) {
      if (this.selectedType === 'locale' && this.selectedValue === locale) {
        this.$reset()
      } else {
        this.selectedType = 'locale'
        this.selectedValue = locale
      }
    },
    selectCategory(category) {
      if (this.selectedType === 'category' && this.selectedValue === category) {
        this.$reset()
      } else {
        this.selectedType = 'category'
        this.selectedValue = category
      }
    },
  },
  persist: {
    storage: sessionStorage,
  },
})

export const useDisplayImageModalStore = defineStore('display-image-modal', {
  state: () => ({
    shown: false,
    object: null,
  }),
  getters: {},
  actions: {
    showImage (object) {
      this.object = object
      this.shown = true
    },
  },
})

export const useDisplayImageGalleryModalStore = defineStore('display-image-gallery-modal', {
  state: () => ({
    shown: false,
    objects: [],
    galleryIndex: null,
  }),
  getters: {},
  actions: {
    showGalleryImage (galleryIndex, objects) {
      this.objects = objects
      this.shown = true
      this.galleryIndex = galleryIndex
    },
  },
  persist: false,
})

export const useInfoModalStore = defineStore('display-info-modal', {
  state: () => ({
    objectId: null,
    objectType: null,
    open: false,
  }),
  getters: {},
  actions: {
    showModal(objectType, objectId) {
      this.objectType = objectType
      this.objectId = objectId
      this.open = true
    },
    reset() {
      this.$reset()
    },
  },
  persist: false,
})