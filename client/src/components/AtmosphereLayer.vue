<template>
  <div class="atmosphere-layer" aria-hidden="true" ref="fogLayer">
    <img
      src="@/assets/textures/fog-atmosphere.svg"
      alt=""
      class="fog-img"
      loading="eager"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const fogLayer = ref(null)
let rafId = null

function updateFog() {
  const scrollY = window.scrollY
  if (fogLayer.value) {
    fogLayer.value.style.transform = `translateY(${scrollY * 0.02}px)`
  }
  rafId = requestAnimationFrame(updateFog)
}

onMounted(() => {
  rafId = requestAnimationFrame(updateFog)
})

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.atmosphere-layer {
  position: absolute;
  inset: 0;
  z-index: 4;
  opacity: 0.15;
  will-change: transform;
}

.fog-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(30px);
}
</style>
