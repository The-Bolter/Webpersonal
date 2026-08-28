<template>
  <div class="concept-layer" aria-hidden="true">
    <img :src="conceptSrc" alt="" />
  </div>
</template>

<script setup>
import conceptSrc from '../assets/index/concept/index-v1-concept.png'
</script>

<style scoped>
.concept-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.concept-layer img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}
</style>
