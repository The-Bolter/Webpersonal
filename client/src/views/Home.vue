<template>
  <div class="home">
    <HeroSection />
    <AboutSection />
    <ProjectsSection />
    <ResumeSection />
    <WorksSection />
    <ContactSection />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import HeroSection from '../components/HeroSection.vue'
import AboutSection from '../components/AboutSection.vue'
import ProjectsSection from '../components/ProjectsSection.vue'
import ResumeSection from '../components/ResumeSection.vue'
import WorksSection from '../components/WorksSection.vue'
import ContactSection from '../components/ContactSection.vue'

let observer

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('ink-revealed')
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    }
  )

  document.querySelectorAll('.ink-reveal').forEach(el => {
    observer.observe(el)
  })
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>
