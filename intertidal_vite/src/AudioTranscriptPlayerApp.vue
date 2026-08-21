<script setup>
import { ref, computed, useId } from 'vue'
import { WaveformPlayer } from '@arraypress/waveform-player-vue'
import { WaveformPlayer as WaveformPlayerCore } from '@arraypress/waveform-player'

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: false,
  },
  artist: {
    type: String,
    required: false,
  },
  transcripts: {
    type: String,
    required: false,
  },
})

const waveformPlayerRef = ref(null)

const seekFunctionName = `waveform_player_seek_to_${useId()}`.replaceAll('-','_')
console.log('seekFunctionName', seekFunctionName)

window[seekFunctionName] = (seconds) => {
  console.log(seekFunctionName, seconds)
  waveformPlayerRef.value.seekTo(seconds)
  waveformPlayerRef.value.play()
}
const processedTranscripts = computed(() => {
  // matches [00:00:00] (and [1234567890:1:1])
  const regex = /\[(\d+)\:(\d{1,2}):(\d{1,2})\]/g
  return props.transcripts?.replace(regex, (match, p1, p2, p3) => {
    const hours = parseInt(p1)
    const minutes = parseInt(p2) + (hours * 60)
    const seconds = parseInt(p3) + (minutes * 60)
    return `<button class="btn btn-link p-0" onclick="${seekFunctionName}(${seconds})">${p1}:${p2}:${p3}</button>`
  })
})
</script>

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="card-title">{{ title }}</h2>
      <WaveformPlayer
        ref="waveformPlayerRef"
        :url="url" :title="title" :artist="artist"
        preload="metadata"
        waveformStyle="seekbar" layout="default" colorPreset="dark" buttonStyle="circle"
        :singlePlay="true" :enableMediaSession="true" :showControls="true"
        :showInfo="true" :showTime="true" :showHoverTime="true" :showPlaybackSpeed="true"
      />
      <hr class="mt-3" v-if="transcripts">
      <details class="mt-3" v-if="transcripts">
        <summary class="card-title h5 d-flex" title="Click to expand/collapse transcripts">
          Transcripts
        </summary>
        <hr class="mt-3">
        <div class="transcripts" v-html="processedTranscripts" />
      </details>
    </div>
  </div>
</template>

<style scoped>
/* slightly fancy details */
details>summary {
  list-style: none;
  cursor: pointer;
  position: relative;
}
summary::-webkit-details-marker {
  display: none;
}
summary {
  padding-left: 1.5em;
}
summary::before {
  content: ' \F285';
  font-family: "bootstrap-icons";
  position: absolute;
  left: 0.25em;
  top: 0;
  font-weight: bold;
}
details[open] summary::before {
  content: ' \F282';
}
</style>