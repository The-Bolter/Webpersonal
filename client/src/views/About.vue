<template>
  <div class="about-page">
    <!-- Fixed landscape background -->
    <div class="page-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" />
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
import { onMounted, onUnmounted } from 'vue'
import bgSrc from '../assets/pages/about.png'
import AboutSection from '../components/AboutSection.vue'
import { useInkReveal } from '../composables/useInkReveal'

useInkReveal()

onMounted(() => {
  document.documentElement.classList.add('about-page-active')
  document.body.classList.add('about-page-active')
})

onUnmounted(() => {
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
}

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
