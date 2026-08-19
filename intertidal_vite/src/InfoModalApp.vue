<script setup>
import { watch, ref, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useInfoModalStore } from './stores/display.js'
import Person from './components/info_modals/Person.vue'
import Organization from './components/info_modals/Organization.vue'
import LoadingDots from './components/LoadingDots.vue'
import { Modal } from 'bootstrap/dist/js/bootstrap.esm'

const {
  objectId,
  objectType,
  open,
} = storeToRefs(useInfoModalStore())

const bootstrapModal = ref(null)
const modalElRef = ref(null)

watch(open, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    if (open.value) {
      bootstrapModal.value?.show()
    } else {
      bootstrapModal.value?.hide()
    }
  }
})
watch(objectId, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => bootstrapModal.value?.handleUpdate())
  }
})
watch(objectType, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    nextTick(() => bootstrapModal.value?.handleUpdate())
  }
})
const modalShown = () => open.value = true
const modalHidden = () => useInfoModalStore().$reset()

// hack to get tinymce transcript and django template contributors working easily
window.showPersonModal = (id) => {
  if (document.getElementById(`person_${id}`)) {
    document.getElementById(`person_${id}`).scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }
  useInfoModalStore().showModal('person', id)
}
window.showOrganizationModal = (id) => {
  if (document.getElementById(`organization_${id}`)) {
    document.getElementById(`organization_${id}`).scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }
  useInfoModalStore().showModal('organization', id)
}
onMounted(() => {
  nextTick(() => {
    modalElRef.value?.addEventListener('hidden.bs.modal', modalHidden)
    modalElRef.value?.addEventListener('shown.bs.modal', modalShown)
    bootstrapModal.value = new Modal(modalElRef.value)
    if (open.value) { bootstrapModal.value.show() }
  })
})
onUnmounted(() => {
  modalElRef.value?.removeEventListener('hidden.bs.modal', modalHidden)
  modalElRef.value?.addEventListener('shown.bs.modal', modalShown)
  bootstrapModal.value?.dispose()
  bootstrapModal.value = null
  useInfoModalStore().$reset()
})
</script>

<template>
  <div ref="modalElRef" class="modal fade" tabindex="-1">
    <div class="modal-dialog modal-fullscreen-lg-down modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <Suspense v-if="objectType == 'person'">
          <Person :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
        <Suspense v-if="objectType == 'organization'">
          <Organization :objectId="objectId" />
          <template #fallback><LoadingDots /></template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-content {
  min-height: 150px;
}
</style>