<template>
  <div class="concept-layer" aria-hidden="true">
    <img :src="conceptSrc" alt="" fetchpriority="high" />
  </div>
</template>

<script setup>
import conceptSrc from '../assets/index/concept/index-v1-concept.lossless.webp'
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
