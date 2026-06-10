<script setup>
import { useTemplateRef, watch, onUnmounted, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useResourceStore, useResourceFilterStore } from '../stores/resources.js'
import { watchDebounced } from '@vueuse/core'

const entityHoverKey = defineModel('entityHoverKey', { default: null })
const resourceCoordinateMap = defineModel('resourceCoordinateMap', { default: new Map() })
const collaboratorCoordinateMap = defineModel('collaboratorCoordinateMap', { default: new Map() })
const categoryCoordinateMap = defineModel('categoryCoordinateMap', { default: new Map() })

const resourceFilterStore = useResourceFilterStore()
const {
  selectedKey,
} = storeToRefs(resourceFilterStore)

const canvasWrapperEl = useTemplateRef('canvasWrapperEl')
const canvasEl = useTemplateRef('canvasEl')
let drawing = false
const redraw = () => {
  if (!drawing && canvasEl.value) {
    drawing = true
    requestAnimationFrame(() => {
      const ctx = canvasEl.value.getContext("2d")
      // clear canvas
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height)
      for (const [resourceId, resourceCoordinates] of resourceCoordinateMap.value) {
        const resource = useResourceStore().getResource(resourceId)
        const {left: resourceLeft, right: resourceRight, y: resourceY} = resourceCoordinates

        for (const [category, categoryCoordinates] of categoryCoordinateMap.value) {
          const categoryKey = `category_${category}`
          const {left: categoryLeft, y: categoryY} = categoryCoordinates
          if (resource.category_set.has(category)) {
            const isHighlighted = entityHoverKey.value === resource.key || entityHoverKey.value === categoryKey || selectedKey.value === categoryKey
            ctx.lineWidth = isHighlighted ? 2 : 1
            ctx.strokeStyle = isHighlighted ? 'rgba(255,255,255, 0.8)' : 'rgba(200,200,200, 0.3)'
            ctx.fillStyle = 'grey'
            ctx.beginPath()
            ctx.moveTo(resourceRight, resourceY)
            // ctx.bezierCurveTo(
            //   resourceRight + ((categoryLeft - resourceRight) * 3 / 4), resourceY,
            //   resourceRight + ((categoryLeft - resourceRight) * 1 / 4), categoryY,
            //   categoryLeft, categoryY
            // )
            ctx.bezierCurveTo(
              resourceRight + ((categoryLeft - resourceRight) / 2), resourceY,
              resourceRight + ((categoryLeft - resourceRight) / 2), categoryY,
              categoryLeft, categoryY
            )
            ctx.stroke()

            // ctx.fillStyle = "blue"
            // ctx.beginPath()
            // ctx.arc(resourceRight, resourceY, 5, 0, 2 * Math.PI)
            // ctx.arc(categoryLeft, categoryY, 5, 0, 2 * Math.PI)
            // ctx.fill()

            // ctx.fillStyle = "red"
            // ctx.beginPath()
            // ctx.arc(resourceRight + ((categoryLeft - resourceRight) * 3 / 4), resourceY, 5, 0, 2 * Math.PI)
            // ctx.arc(resourceRight + ((categoryLeft - resourceRight) * 1 / 4), categoryY, 5, 0, 2 * Math.PI)
            // ctx.fill()
          }
        }
        for (const [entityKey, collaboratorCoordinates] of collaboratorCoordinateMap.value) {
          const {right: collaboratorRight, y: collaboratorY} = collaboratorCoordinates
          const personId = entityKey.startsWith('person_') ? parseInt(entityKey.slice('person_'.length)) : null
          const organizationId = entityKey.startsWith('organization_') ? parseInt(entityKey.slice('organization_'.length)) : null
          if ((personId && resource.person_id_set.has(personId)) || (organizationId && resource.organization_id_set.has(organizationId))) {
            const isHighlighted = entityHoverKey.value === resource.key || entityHoverKey.value === entityKey || selectedKey.value === entityKey
            ctx.lineWidth = isHighlighted ? 2 : 1
            ctx.strokeStyle = isHighlighted ? 'rgba(255,255,255, 0.8)' : 'rgba(200,200,200, 0.3)'
            ctx.beginPath()
            ctx.moveTo(resourceLeft, resourceY)
            ctx.bezierCurveTo(
              resourceLeft - ((resourceLeft - collaboratorRight) / 2), resourceY,
              resourceLeft - ((resourceLeft - collaboratorRight) / 2), collaboratorY,
              collaboratorRight, collaboratorY
            )
            ctx.stroke()
          }
        }
      }
    })
    drawing = false
  }
}
const setupCanvas = () => {
  canvasEl.value.width = canvasWrapperEl.value.clientWidth
  canvasEl.value.height = canvasWrapperEl.value.clientHeight
  redraw()
}
let animatedRedrawTimeouts = []
const animatedRedraw = () => {
  animatedRedrawTimeouts.forEach((redrawTimeout) => clearTimeout(redrawTimeout))
  animatedRedrawTimeouts = [...Array(20)].map((_, index) => setTimeout(redraw, (index)*50))
}
const handleScroll = () => animatedRedraw()
const handleResize = () => nextTick(() => setupCanvas())
watch(selectedKey, (newValue, oldValue) => {
  if (newValue !== oldValue) { nextTick(() => animatedRedraw()) }
})
watch(entityHoverKey, (newValue, oldValue) => {
  if (newValue !== oldValue) { animatedRedraw() }
})
watchDebounced(resourceCoordinateMap, (newValue, oldValue) => {
  if (newValue !== oldValue) { animatedRedraw() }
},{ debounce: 10, maxWait: 50, deep: true })
watchDebounced(categoryCoordinateMap, (newValue, oldValue) => {
  if (newValue !== oldValue) { animatedRedraw() }
},{ debounce: 10, maxWait: 50, deep: true })
watchDebounced(collaboratorCoordinateMap, (newValue, oldValue) => {
  if (newValue !== oldValue) { animatedRedraw() }
},{ debounce: 10, maxWait: 50, deep: true })
onMounted(() => {
  setupCanvas()
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="canvasWrapperEl" class="position-fixed top-0 bottom-0 start-0 end-0 ">
    <canvas ref="canvasEl" />
  </div>
</template>

<style scoped>
</style>