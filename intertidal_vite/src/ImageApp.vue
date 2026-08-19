<script setup>
import { useDisplayImageModalStore } from './stores/display.js'

const props = defineProps({
  image: { type: String, required: true },
  thumbnail: { type: String, required: true },
  label: { type: String },
  class: { type: String },
})
</script>

<template>
  <img
    :src="thumbnail"
    :alt="label || ''"
    :class="class"
    loading="lazy" fetchpriority="low"
    @click="() => useDisplayImageModalStore().showImage({image, label})"
  >
</template>

<style lang="scss" scoped>
img {
  cursor: pointer;
}
</style>