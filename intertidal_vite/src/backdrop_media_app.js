import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import BackdropMediaApp from './BackdropMediaApp.vue'
import VideoPlayer from '@videojs-player/vue'

// make sure videojs plugins are working
import 'video.js'
import 'videojs-theme-kit/videojs-skin.min.js'

import './assets/backdrop_media.scss'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const mountElList = document.querySelectorAll('#backdrop-media-app')
mountElList.forEach((mountEl) => {
  const app = createApp(BackdropMediaApp, { ...mountEl.dataset })
  app.use(pinia)
  app.use(VideoPlayer)
  app.mount(mountEl)
})
