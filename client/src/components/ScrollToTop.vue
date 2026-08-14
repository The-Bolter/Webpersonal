<template>
  <button
    v-show="visible"
    class="scroll-top"
    @click="scrollToTop"
    aria-label="Scroll to top"
  >
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
      <path d="M18 15l-6-6-6 6"/>
    </svg>
  </button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const visible = ref(false)
let rafPending = false

function onScroll() {
  if (rafPending) return
  rafPending = true
  requestAnimationFrame(() => {
    rafPending = false
    visible.value = window.scrollY > 800
  })
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.scroll-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 900;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(251, 246, 238, 0.7);
  border: 1px solid rgba(139, 132, 120, 0.15);
  color: var(--ink-light);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color var(--dur-base) var(--ease-out),
              color var(--dur-base) var(--ease-out),
              background var(--dur-base) var(--ease-out);
}

.scroll-top:hover {
  border-color: var(--bark);
  color: var(--ink-dark);
  background: rgba(255, 254, 250, 0.9);
}
</style>
