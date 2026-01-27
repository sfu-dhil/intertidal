<script setup>
import BackdropVideoPlayerWrapper from './components/BackdropVideoPlayerWrapper.vue'

const props = defineProps({
  videoSrc: {
    type: String,
  },
  imageSrc: {
    type: String,
  },
})
</script>

<template>
  <BackdropVideoPlayerWrapper v-if="videoSrc" :video="videoSrc" class="object-fit-fill w-100 h-100 backdrop-opacity"></BackdropVideoPlayerWrapper>
  <img v-if="!videoSrc && imageSrc" :src="imageSrc" class="object-fit-fill w-100 h-100 backdrop-opacity" alt="Background Image">
</template>

<style scoped>
  .backdrop-opacity {
    opacity: 0;
    animation: fadeIn 2s forwards;
  }
  @keyframes fadeIn {
      to {
          opacity: 0.6;
      }
  }
</style>