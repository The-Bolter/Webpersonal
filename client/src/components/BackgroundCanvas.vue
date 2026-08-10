<template>
  <div class="background-system" aria-hidden="true">
    <!-- Layer 1: Tall poster — scroll down → poster shifts UP → lower parts revealed -->
    <div class="bg-poster-wrap">
      <img
        src="/bg-poster.png"
        alt=""
        class="poster-img"
        ref="posterImg"
        loading="eager"
      />
    </div>

    <!-- Layer 2: Warm veil -->
    <div class="bg-layer bg-warm-veil"></div>

    <!-- Layer 3: Ink overlays -->
    <InkOverlay />

    <!-- Layer 4: Atmosphere fog -->
    <AtmosphereLayer />

    <!-- Layer 5: Film grain -->
    <div class="bg-layer bg-grain">
      <img src="@/assets/textures/grain.svg" alt="" class="bg-img-full" loading="eager" />
    </div>

    <!-- Layer 6: Edge vignette -->
    <div class="bg-layer bg-vignette">
      <img src="@/assets/textures/vignette.svg" alt="" class="bg-img-full" loading="eager" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import InkOverlay from './InkOverlay.vue'
import AtmosphereLayer from './AtmosphereLayer.vue'

const posterImg = ref(null)
let rafId = null

function parallaxScroll() {
  if (posterImg.value) {
    const scrollY = window.scrollY
    // Scroll down → poster shifts UP (negative) → reveals lower parts
    // No clamp — poster container is tall enough to scroll through full page
    const shift = scrollY * 0.22
    posterImg.value.style.transform = `translate3d(0, ${-shift}px, 0)`
  }
  rafId = requestAnimationFrame(parallaxScroll)
}

onMounted(() => { rafId = requestAnimationFrame(parallaxScroll) })
onUnmounted(() => { if (rafId) cancelAnimationFrame(rafId) })
</script>

<style scoped>
.background-system {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.bg-layer {
  position: absolute;
  inset: 0;
}

/* Layer 1: Poster — 2x viewport tall, shifts UP on scroll */
.bg-poster-wrap {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 280vh;
  z-index: 1;
}

.poster-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  image-rendering: -webkit-optimize-contrast;
  backface-visibility: hidden;
  will-change: transform;
}

/* Layer 2: Warm veil */
.bg-warm-veil {
  z-index: 2;
  background: rgba(229, 213, 189, 0.15);
}

/* Layer 5: Grain */
.bg-grain {
  position: fixed;
  z-index: 5;
  mix-blend-mode: soft-light;
  opacity: 0.18;
}

.bg-img-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Layer 6: Vignette */
.bg-vignette {
  z-index: 6;
  mix-blend-mode: multiply;
  opacity: 0.35;
}
</style>
