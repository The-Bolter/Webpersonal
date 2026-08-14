<template>
  <div class="background-system" aria-hidden="true">
    <!-- Layer 1: Warm veil -->
    <div class="bg-layer bg-warm-veil"></div>

    <!-- Layer 2: Ink overlays -->
    <InkOverlay />

    <!-- Layer 3: Atmosphere fog -->
    <AtmosphereLayer />

    <!-- Layer 4: Film grain -->
    <div class="bg-layer bg-grain">
      <img src="@/assets/textures/grain.svg" alt="" class="bg-img-full" loading="eager" />
    </div>

    <!-- Layer 5: Edge vignette -->
    <div class="bg-layer bg-vignette">
      <img src="@/assets/textures/vignette.svg" alt="" class="bg-img-full" loading="eager" />
    </div>
  </div>
</template>

<script setup>
import InkOverlay from './InkOverlay.vue'
import AtmosphereLayer from './AtmosphereLayer.vue'
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

/* Layer 1: Warm veil */
.bg-warm-veil {
  z-index: 2;
  background: rgba(229, 213, 189, 0.15);
}

/* Layer 4: Grain */
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

/* Layer 5: Vignette */
.bg-vignette {
  z-index: 6;
  mix-blend-mode: multiply;
  opacity: 0.35;
}
</style>
