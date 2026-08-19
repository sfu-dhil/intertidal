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
import AudioTranscriptPlayerApp from './AudioTranscriptPlayerApp.vue'
import ImageApp from './ImageApp.vue'
import ImageModalApp from './ImageModalApp.vue'
import ImageGalleryApp from './ImageGalleryApp.vue'
import ImageGalleryModalApp from './ImageGalleryModalApp.vue'
import InfoModalApp from './InfoModalApp.vue'

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
    const app = createApp(ResourcesApp, { ...mountEl.dataset })
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

  document.querySelectorAll('.audio-transcript-player-app').forEach((mountEl) => {
    const app = createApp(AudioTranscriptPlayerApp, { ...mountEl.dataset })
    app.use(pinia)
    app.config.idPrefix = 'audio-transcript-player-app'
    app.mount(mountEl)
  })

  document.querySelectorAll('.image-app').forEach((mountEl) => {
    const app = createApp(ImageApp, { ...mountEl.dataset })
    app.use(pinia)
    app.mount(mountEl)
  })

  document.querySelectorAll('#image-model-app').forEach((mountEl) => {
    const app = createApp(ImageModalApp, { ...mountEl.dataset })
    app.use(pinia)
    app.mount(mountEl)
  })

  document.querySelectorAll('.image-gallery-app').forEach((mountEl) => {
    const app = createApp(ImageGalleryApp, {
      images: mountEl.dataset.imagesJson ? JSON.parse(mountEl.dataset.imagesJson) : [],
    })
    app.use(pinia)
    app.mount(mountEl)
  })

  document.querySelectorAll('#image-gallery-model-app').forEach((mountEl) => {
    const app = createApp(ImageGalleryModalApp, { ...mountEl.dataset })
    app.use(pinia)
    app.mount(mountEl)
  })

  document.querySelectorAll('#info-modal-app').forEach((mountEl) => {
    const app = createApp(InfoModalApp)
    app.use(pinia)
    app.mount(mountEl)
  })
})
