<script setup>
import { useOrganizationsStore } from '../../stores/data.js'

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
})

const object = await useOrganizationsStore().getById(props.objectId)
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="object.label" />
          <figcaption class="blockquote-footer" v-if="object.address" v-html="object.address" />
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body">
    <div class="card-text" v-if="object.alternative_names.length > 0">
      <div class="fw-bold">Alternative Names</div>
      <div v-for="alternative_name in object.alternative_names">{{ alternative_name }}</div>
    </div>
    <div class="card-text mt-3" v-if="object.links.length > 0">
      <div class="fw-bold">Links</div>
      <div v-for="link in object.links">
        <a target="_blank" :href="link">{{ link }}</a>
      </div>
    </div>
  </div>
</template>
<style scoped>
</style>