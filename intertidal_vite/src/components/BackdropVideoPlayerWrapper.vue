<script setup>
import { computed } from 'vue'

const video = defineModel('video')

const isSafari = () => {
  const userAgent = navigator.userAgent;
  return userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1;
}

const videoSources = computed(() => {
  if (!video.value) {
    return []
  }
  const sources = [{
    src: video.value,
    type: 'application/dash+xml',
  }, {
    // we get a HLS playlist for free when generating the mpeg-dash with ffmpeg
    src: video.value.replace(/\/[^\/]+$/, '/master.m3u8'),
    type: 'application/x-mpegURL',
  }]
  return isSafari() ? sources.reverse() : sources
})
const videoPluginOptions = computed(() => {
  const pluginOptions = {
    qualityLevels: {},
    theme: { skin: 'slate' },
  }
  return pluginOptions
})
const videoHtml5Options = computed(() => {
  const html5Options = {}
  if (isSafari()) {
    html5Options.nativeTextTracks = false
    html5Options.nativeAudioTracks = false
    // html5Options.nativeVideoTracks = false
  }
  return html5Options
})
</script>

<template>
  <video-player
    :sources="videoSources"
    :controls="false" :fill="true"
    :autoplay="true" :loop="true" :muted="true"
    :disablePictureInPicture="true"
    :plugins="videoPluginOptions"
    :html5="videoHtml5Options"
  >
  </video-player>
</template>

<style lang="scss" scoped>
  :deep() {
    .vjs-big-play-button {
      display: none !important;
    }
    video {
      object-fit: cover;
    }
  }
</style>


