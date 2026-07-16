<script setup>
import { ref, computed, onMounted } from 'vue'
import { WaveformPlayer } from '@arraypress/waveform-player-vue'

const props = defineProps({
  playlist: {
    type: Array,
    required: true,
  },
})

const waveformPlayerRefs = ref([])

const playNextOnEnd = (currentIndex) => {
  if (waveformPlayerRefs.value?.length > currentIndex + 1) {
    const nextPlayer = waveformPlayerRefs.value[currentIndex+1]
    nextPlayer.seekTo(0)
    nextPlayer.play()
  }
}
</script>

<template>
  <ol class="list-group">
    <li
      v-for="(item, itemIndex) in playlist" :key="item.url"
      class="list-group-item d-flex justify-content-between align-items-start"
    >
      <div class="flex-grow-1 mx-2">
        <WaveformPlayer
          ref="waveformPlayerRefs"
          :url="item.url" :title="item.title"
          preload="metadata"
          waveformStyle="seekbar" layout="default" colorPreset="dark" buttonStyle="circle"
          :singlePlay="true" :enableMediaSession="true" :showControls="true"
          :showInfo="true" :showTime="true" :showHoverTime="true"
          @end="() => playNextOnEnd(itemIndex)"
        />
      </div>
      <div class="action-items align-self-center text-center">
        <a
          v-if="item.resource_url"
          class="icon-link icon-link-hover"
          :href="item.resource_url"
        >
          View
          <i class="bi bi-arrow-right"></i>
        </a>
      </div>
    </li>
  </ol>
</template>

<style scoped>
.action-items {
  width: 5em;
}
</style>