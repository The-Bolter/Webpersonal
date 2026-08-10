<template>
  <div class="project-card" @mousemove="onTilt" @mouseleave="resetTilt" ref="card">
    <div class="card-image">
      <div class="image-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
          <line x1="8" y1="21" x2="16" y2="21"/>
          <line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
      </div>
      <div class="card-overlay">
        <div class="overlay-links">
          <a v-if="project.github" :href="project.github" target="_blank" rel="noopener" class="overlay-link" @click.stop>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            Code
          </a>
          <a v-if="project.demo" :href="project.demo" target="_blank" rel="noopener" class="overlay-link" @click.stop>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            Demo
          </a>
        </div>
      </div>
    </div>

    <div class="card-body">
      <h3 class="card-title">{{ project.title }}</h3>
      <p class="card-desc">{{ project.description }}</p>
      <div class="card-tags">
        <span v-for="tag in project.tags" :key="tag" class="card-tag">{{ tag }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  project: { type: Object, required: true }
})

const card = ref(null)

function onTilt(e) {
  if (!card.value) return
  const rect = card.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const rotateX = (y - centerY) / 20
  const rotateY = (centerX - x) / 20
  card.value.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02,1.02,1.02)`
}

function resetTilt() {
  if (!card.value) return
  card.value.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1,1,1)'
}
</script>

<style scoped>
.project-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  transform-style: preserve-3d;
}

.project-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: rgba(161, 134, 111, 0.35);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(47, 62, 47, 0.15), rgba(161, 134, 111, 0.15));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(47, 62, 47, 0.88);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-card:hover .card-overlay {
  opacity: 1;
}

.overlay-links {
  display: flex;
  gap: var(--spacing-md);
}

.overlay-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  color: #fff;
  background: var(--gradient-primary);
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  transition: transform 0.2s ease;
}

.overlay-link:hover {
  transform: translateY(-2px);
}

.card-body {
  padding: var(--spacing-xl);
}

.card-title {
  font-size: 1.15rem;
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
}

.card-desc {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  line-height: 1.7;
  margin-bottom: var(--spacing-lg);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.card-tag {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  color: var(--color-primary);
  background: rgba(47, 62, 47, 0.06);
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  letter-spacing: 0.01em;
}
</style>
