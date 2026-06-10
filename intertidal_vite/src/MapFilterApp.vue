<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceFilterStore } from './stores/resources.js'

const resourceFilterStore = useResourceFilterStore()
const {
  selectedType,
  selectedValue
} = storeToRefs(resourceFilterStore)

const websiteOrigin = window.location.origin
const isVancouverSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'VANCOUVER')
const isHongKongSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'HONG_KONG')
const isSingaporeSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'SINGAPORE')
</script>

<template>
  <div class="ratio ratio-16x9 my-5 position-relative">
    <img :src="websiteOrigin+'/static/images/watercolors/map.png'" class="img-fluid position-absolute" alt="Watercolor Map z-0" />
    <div class="vancouver-marker map-marker position-absolute z-1">
      <div
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{ 'border-white': !isVancouverSelected, 'border-primary': isVancouverSelected }"
        @click="useResourceFilterStore().selectLocale('VANCOUVER')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/vancouver.png'" class="rounded-circle m-0 p-0" alt="Vancouver Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1" :class="{ 'text-white': !isVancouverSelected, 'text-primary': isVancouverSelected }">
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
    <div class="hong-kong-marker map-marker position-absolute z-1">
      <div
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{ 'border-white': !isHongKongSelected, 'border-primary': isHongKongSelected }"
        @click="useResourceFilterStore().selectLocale('HONG_KONG')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/hong_kong.png'" class="rounded-circle m-0 p-0" alt="Hong Kong Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1" :class="{ 'text-white': !isHongKongSelected, 'text-primary': isHongKongSelected }">
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
    <div class="singapore-marker map-marker position-absolute z-1">
      <div
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{ 'border-white': !isSingaporeSelected, 'border-primary': isSingaporeSelected }"
        @click="useResourceFilterStore().selectLocale('SINGAPORE')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/singapore.png'" class="rounded-circle m-0 p-0" alt="Singapore Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1" :class="{ 'text-white': !isSingaporeSelected, 'text-primary': isSingaporeSelected }">
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-marker {
  cursor: pointer;
  width: fit-content;
  height: fit-content;
  transform: translate(-50%,-100%) !important;
  z-index: 10000 !important; /* fix issue with being under the audio player */

  > div {
    width: fit-content;
    height: fit-content;
    > img {
      width: 150px;
    }
  }
  &.vancouver-marker {
    top: 27.75%;
    left: 73.5%;
  }
  &.hong-kong-marker {
    top: 53.75%;
    left: 19.5%;
  }
  &.singapore-marker {
    top: 71.1%;
    left: 14.4%;
  }
}
@media (max-width: 768px) {
  .map-marker > div > img {
      width: 50px;
  }
}
@media (min-width: 769px) and (max-width: 992px) {
  .map-marker > div > img {
      width: 75px;
  }
}
@media (min-width: 993px) and (max-width: 1200px) {
  .map-marker > div > img {
      width: 100px;
  }
}
@media (min-width: 1201px) {
  .map-marker > div > img {
      width: 125px;
  }
}
</style>