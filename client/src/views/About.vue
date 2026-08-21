<template>
  <div class="about-page">
    <!-- Fixed landscape background -->
    <div class="page-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" />
    </div>

    <!-- Subtle readability veil -->
    <div class="page-veil" aria-hidden="true"></div>

    <!-- Content -->
    <div class="page-content">
      <AboutSection />
    </div>
  </div>
</template>

<script setup>
import bgSrc from '../assets/pages/about.png'
import AboutSection from '../components/AboutSection.vue'
import { useInkReveal } from '../composables/useInkReveal'

useInkReveal()
</script>

<style scoped>
.about-page {
  position: relative;
  min-height: 100vh;
}

.page-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.page-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.page-veil {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: rgba(245, 236, 222, 0.28);
}

.page-content {
  position: relative;
  z-index: 1;
}
</style>
