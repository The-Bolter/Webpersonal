<template>
  <div class="about-page">
    <!-- Fixed landscape background -->
    <div class="page-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" :class="{ 'is-ready': backgroundReady }" />
    </div>

    <!-- Subtle readability veil -->
    <div class="page-veil" aria-hidden="true"></div>

    <!-- Content (independent scroll layer) -->
    <div class="page-content" data-lenis-prevent>
      <AboutSection />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import bgSrc from '../assets/pages/about.png'
import AboutSection from '../components/AboutSection.vue'
import { useInkReveal } from '../composables/useInkReveal'
import { waitForVisualGroup } from '../composables/useVisualPreload'

useInkReveal()
const backgroundReady = ref(false)
let isActive = true

onMounted(() => {
  waitForVisualGroup([bgSrc], 1800).then(() => {
    if (isActive) backgroundReady.value = true
  })
  document.documentElement.classList.add('about-page-active')
  document.body.classList.add('about-page-active')
})

onUnmounted(() => {
  isActive = false
  document.documentElement.classList.remove('about-page-active')
  document.body.classList.remove('about-page-active')
})
</script>

<style scoped>
.about-page {
  position: relative;
  height: 100dvh;
  min-height: 100dvh;
  overflow: hidden;
}

.page-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.page-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  opacity: 0;
  transition: opacity 0.55s ease;
}
.page-bg img.is-ready { opacity: 1; }

.page-veil {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: rgba(245, 236, 222, 0.28);
}

.page-content {
  position: relative;
  z-index: 1;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.page-content::-webkit-scrollbar {
  width: 4px;
}
.page-content::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.25);
  border-radius: 2px;
}
</style>
