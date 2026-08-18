// vuejs
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Multiselect from 'vue-multiselect'
import { MotionPlugin } from '@vueuse/motion'
import BackdropMediaApp from './BackdropMediaApp.vue'
import VideoPlayer from '@videojs-player/vue'
import ResourcesApp from './ResourcesApp.vue'
import MapFilterApp from './MapFilterApp.vue'
import AudioPlayerApp from './AudioPlayerApp.vue'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// css
import './assets/intertidal.scss'

// bootstrap
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// other
// make sure videojs plugins are working
import 'video.js'
import 'videojs-theme-kit/videojs-skin.min.js'

const ready = (fn) => document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn)
ready(() => {
  document.querySelectorAll('#backdrop-media-app').forEach((mountEl) => {
    const app = createApp(BackdropMediaApp, { ...mountEl.dataset })
    app.use(pinia)
    app.use(VideoPlayer)
    app.mount(mountEl)
  })

  document.querySelectorAll('#resources-app').forEach((mountEl) => {
    const app = createApp(ResourcesApp, {
      resources: mountEl.dataset.resourcesJson ? JSON.parse(mountEl.dataset.resourcesJson) : [],
      people: mountEl.dataset.peopleJson ? JSON.parse(mountEl.dataset.peopleJson) : [],
      organizations: mountEl.dataset.organizationsJson ? JSON.parse(mountEl.dataset.organizationsJson) : [],
      marcRelators: mountEl.dataset.marcRelatorsJson ? JSON.parse(mountEl.dataset.marcRelatorsJson) : [],
    })
    app.use(pinia)
    app.use(MotionPlugin)
    app.component('Multiselect', Multiselect)
    app.mount(mountEl)
  })

  document.querySelectorAll('#map-filter-app').forEach((mountEl) => {
    const app = createApp(MapFilterApp)
    app.use(pinia)
    app.use(MotionPlugin)
    app.mount(mountEl)
  })

  document.querySelectorAll('.audio-player-app').forEach((mountEl) => {
    const app = createApp(AudioPlayerApp, {
      playlist: mountEl.dataset.playlistJson ? JSON.parse(mountEl.dataset.playlistJson) : [],
    })
    app.use(pinia)
    app.mount(mountEl)
  })
})
