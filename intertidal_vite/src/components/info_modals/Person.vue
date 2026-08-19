<script setup>
import { usePeopleStore } from '../../stores/data.js'
import { useDisplayImageModalStore } from '../../stores/display.js'
import ImageApp from '../../ImageApp.vue'

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
})

const object = await usePeopleStore().getById(props.objectId)
</script>

<template>
  <div class="modal-header align-items-start pb-0">
    <div class="modal-title">
      <figure>
        <blockquote class="blockquote">
          <h1 v-html="object.label" />
          <figcaption class="blockquote-footer" v-for="alternative_name in object.alternative_names" v-html="alternative_name" />
        </blockquote>
      </figure>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body p-0">
    <div class="row g-0 p-0 m-0">
      <div class="col-md-3" v-if="object.image && object.thumbnail">
        <ImageApp :image="object.image" :thumbnail="object.thumbnail" :label="object.label" class="img-fluid object-fit-cover" />
      </div>
      <div class="p-3" :class="{'col-md-9': object.thumbnail}">
        <div class="card-text" v-html="object.bio" />
        <div class="card-text" v-if="object.links.length > 0">
          <div class="fw-bold">Links</div>
          <div v-for="link in object.links">
            <a target="_blank" :href="link">{{ link }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
</style>