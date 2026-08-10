<template>
  <div class="loading-screen" :class="{ hidden: !store.isLoading }">
    <div class="loading-content">
      <div class="loading-logo">The Curator's Log</div>
    </div>
  </div>
</template>

<script setup>
import { useAppStore } from '../store'
const store = useAppStore()
</script>

<style scoped>
.loading-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--paper);
  transition: opacity 0.8s var(--ease-out), visibility 0.8s var(--ease-out);
}

.loading-screen.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.loading-content { text-align: center; }

.loading-logo {
  font-family: var(--font-editorial);
  font-size: 1.8rem;
  color: var(--ink-green);
  animation: inkFade 3s ease-in-out infinite;
}

@keyframes inkFade {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
</style>
