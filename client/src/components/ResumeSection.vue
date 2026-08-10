<template>
  <section id="resume" class="resume-section">
    <div class="container">
      <div class="resume-header ink-reveal">
        <p class="editorial-label">Provenance</p>
        <h2 class="editorial-title">
          A Quiet<br><em>Journey</em>
        </h2>
      </div>

      <!-- Timeline �?sparse, editorial -->
      <div class="provenance-timeline ink-reveal ink-reveal-delay-1">
        <div v-for="section in store.resume.sections" :key="section.title" class="timeline-block">
          <h3 class="timeline-block-title">{{ section.title }}</h3>
          <div class="timeline-items">
            <div v-for="item in section.items" :key="item.role" class="timeline-item museum-label">
              <span class="timeline-period">{{ item.period }}</span>
              <h4>{{ item.role }}</h4>
              <p class="timeline-org">{{ item.company }}</p>
              <p class="timeline-note">{{ item.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useAppStore } from '../store'
const store = useAppStore()
</script>

<style scoped>
.resume-section {
  padding: var(--space-section) 0;
}

.resume-header {
  margin-bottom: var(--space-3xl);
  max-width: 500px;
}

.provenance-timeline {
  max-width: 600px;
}

.timeline-block {
  margin-bottom: var(--space-3xl);
}

.timeline-block-title {
  font-family: var(--font-editorial);
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--ink-dark);
  letter-spacing: 0.05em;
  margin-bottom: var(--space-xl);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid rgba(139, 132, 120, 0.15);
}

.timeline-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.timeline-item {
  max-width: 520px;
}

.timeline-period {
  font-family: var(--font-label);
  font-size: 0.65rem;
  color: var(--bark);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  display: block;
  margin-bottom: var(--space-xs);
}

.timeline-item h4 {
  font-family: var(--font-editorial);
  font-size: 1.15rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin-bottom: var(--space-xs);
}

.timeline-org {
  font-size: 0.88rem;
  color: var(--ink-light);
  margin-bottom: var(--space-md);
}

.timeline-note {
  font-size: 0.85rem;
  color: var(--ink-light);
  line-height: 1.8;
  margin: 0;
}

@media (max-width: 768px) {
  .provenance-timeline { max-width: 100%; }
  .timeline-item { max-width: 100%; }
}
</style>
