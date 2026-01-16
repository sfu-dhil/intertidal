import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ResourcesApp from './ResourcesApp.vue'

import './assets/base.css'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(ResourcesApp)
app.use(pinia)
app.mount('#resources-app')
