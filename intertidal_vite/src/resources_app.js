import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ResourcesApp from './ResourcesApp.vue'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const mountElList = document.querySelectorAll('#resources-app')
mountElList.forEach((mountEl) => {
  const app = createApp(ResourcesApp, {
    resources: mountEl.dataset.resourcesJson ? JSON.parse(mountEl.dataset.resourcesJson) : [],
    people: mountEl.dataset.peopleJson ? JSON.parse(mountEl.dataset.peopleJson) : [],
    organizations: mountEl.dataset.organizationsJson ? JSON.parse(mountEl.dataset.organizationsJson) : [],
  })
  app.use(pinia)
  app.mount(mountEl)
})
