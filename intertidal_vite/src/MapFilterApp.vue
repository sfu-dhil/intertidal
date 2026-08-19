<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useMouseInElement } from '@vueuse/core'
import { useResourcesFilterStore } from './stores/display.js'

const {
  selectedType,
  selectedValue,
} = storeToRefs(useResourcesFilterStore())

const vancouverMarkerCircleRef = ref(null)
const hongKongMarkerCircleRef = ref(null)
const singaporeMarkerCircleRef = ref(null)

const websiteOrigin = window.location.origin
const isVancouverSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'VANCOUVER')
const { isOutside: isOutsideVancouverMarker } = useMouseInElement(vancouverMarkerCircleRef)
const isHongKongSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'HONG_KONG')
const { isOutside: isOutsideHongKongMarker } = useMouseInElement(hongKongMarkerCircleRef)
const isSingaporeSelected = computed(() => selectedType.value === 'locale' && selectedValue.value === 'SINGAPORE')
const { isOutside: isOutsideSingaporeMarker } = useMouseInElement(singaporeMarkerCircleRef)
</script>

<template>
  <div class="ratio ratio-16x9 my-5 position-relative">
    <img :src="websiteOrigin+'/static/images/watercolors/map.png'" class="img-fluid position-absolute watercolor-map-img" alt="Watercolor Map z-0" />
    <div class="vancouver-marker map-marker position-absolute z-1">
      <div
        ref="vancouverMarkerCircleRef"
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{
          'border-white': !isVancouverSelected && isOutsideVancouverMarker,
          'border-primary': isVancouverSelected && isOutsideVancouverMarker,
          'border-info': !isOutsideVancouverMarker
        }"
        @click="useResourcesFilterStore().selectLocale('VANCOUVER')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/vancouver.png'" class="rounded-circle m-0 p-0 watercolor-map-icon-img" alt="Vancouver Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1"
          :class="{
            'text-white': !isVancouverSelected && isOutsideVancouverMarker,
            'text-primary': isVancouverSelected && isOutsideVancouverMarker,
            'text-info': !isOutsideVancouverMarker,
          }"
        >
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
    <div class="hong-kong-marker map-marker position-absolute z-1">
      <div
        ref="hongKongMarkerCircleRef"
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{
          'border-white': !isHongKongSelected && isOutsideHongKongMarker,
          'border-primary': isHongKongSelected && isOutsideHongKongMarker,
          'border-info': !isOutsideHongKongMarker
        }"
        @click="useResourcesFilterStore().selectLocale('HONG_KONG')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/hong_kong.png'" class="rounded-circle m-0 p-0 watercolor-map-icon-img" alt="Hong Kong Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1"
          :class="{
            'text-white': !isHongKongSelected && isOutsideHongKongMarker,
            'text-primary': isHongKongSelected && isOutsideHongKongMarker,
            'text-info': !isOutsideHongKongMarker,
          }"
        >
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
    <div class="singapore-marker map-marker position-absolute z-1">
      <div
        ref="singaporeMarkerCircleRef"
        v-motion-slide-visible-top
        class="border border-3 rounded-circle position-relative"
        :class="{
          'border-white': !isSingaporeSelected && isOutsideSingaporeMarker,
          'border-primary': isSingaporeSelected && isOutsideSingaporeMarker,
          'border-info': !isOutsideSingaporeMarker
        }"
        @click="useResourcesFilterStore().selectLocale('SINGAPORE')"
      >
        <img :src="websiteOrigin+'/static/images/watercolors/singapore.png'" class="rounded-circle m-0 p-0 watercolor-map-icon-img" alt="Singapore Watercolor Marker" />
        <span class="position-absolute z-2 top-100 start-50 translate-middle mt-1"
          :class="{
            'text-white': !isSingaporeSelected && isOutsideSingaporeMarker,
            'text-primary': isSingaporeSelected && isOutsideSingaporeMarker,
            'text-info': !isOutsideSingaporeMarker,
          }"
        >
          <i class="bi bi-caret-down-fill"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.watercolor-map-img,
.watercolor-map-icon-img {
  /* filter: grayscale(0.65); */
  filter: saturate(0.4);
}
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