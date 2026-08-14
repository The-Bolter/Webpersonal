<template>
  <AboutSection />
</template>

<script setup>
import { useInkReveal } from '../composables/useInkReveal'
import AboutSection from '../components/AboutSection.vue'

useInkReveal()
</script>
