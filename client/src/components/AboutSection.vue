<template>
  <section id="about" class="about-section">
    <div class="container">
      <!-- Section header — placed at top-left, editorial style -->
      <div class="about-header ink-reveal">
        <p class="editorial-label">On Philosophy</p>
        <h2 class="editorial-title">
          Rooted in<br><em>Contemplation</em>
        </h2>
      </div>

      <!-- Philosophy cards — sparse, only 3 items, wide spacing -->
      <div class="philosophy-row">
        <div
          v-for="(item, i) in store.profile.philosophy"
          :key="item.title"
          class="philosophy-label-card museum-label ink-reveal"
          :class="`ink-reveal-delay-${i + 1}`"
        >
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </div>
      </div>

      <!-- Bio — narrow, poetic, maximum ~40 chars per line -->
      <div class="about-bio ink-reveal ink-reveal-delay-3">
        <p v-for="(paragraph, i) in store.profile.bio" :key="i">{{ paragraph }}</p>
      </div>

      <!-- Disciplines — comma separated, editorial style -->
      <div class="about-disciplines ink-reveal ink-reveal-delay-3">
        <p class="disciplines-label">Disciplines</p>
        <p class="disciplines-list">
          {{ store.profile.skills.join(' &middot; ') }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useAppStore } from '../store'
const store = useAppStore()
</script>

<style scoped>
.about-section {
  padding: var(--space-section) 0;
}

.about-header {
  margin-bottom: var(--space-3xl);
  max-width: 500px;
}

/* Philosophy cards — generous spacing */
.philosophy-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-2xl);
  margin-bottom: var(--space-4xl);
}

.philosophy-label-card {
  max-width: 320px;
}

.philosophy-label-card h3 {
  font-family: var(--font-editorial);
  font-size: 1.3rem;
  font-weight: 500;
  color: var(--ink-dark);
  margin-bottom: var(--space-md);
  letter-spacing: 0.04em;
}

.philosophy-label-card p {
  font-size: 0.88rem;
  color: var(--ink-light);
  line-height: 1.85;
  margin: 0;
}

/* Bio — narrow, centered, poetic measure */
.about-bio {
  max-width: 560px;
  margin-bottom: var(--space-3xl);
}

.about-bio p {
  font-size: 1rem;
  line-height: 2;
  color: var(--ink-light);
  margin-bottom: var(--space-lg);
}

/* Disciplines — editorial comma list */
.about-disciplines {
  padding-top: var(--space-2xl);
  border-top: 1px solid rgba(139, 132, 120, 0.12);
}

.disciplines-label {
  font-family: var(--font-label);
  font-size: 0.65rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.16em;
  margin-bottom: var(--space-sm);
}

.disciplines-list {
  font-family: var(--font-editorial);
  font-size: 1rem;
  color: var(--ink-light);
  letter-spacing: 0.04em;
  margin: 0;
}

@media (max-width: 768px) {
  .philosophy-row { grid-template-columns: 1fr; gap: var(--space-xl); }
  .about-bio { max-width: 100%; }
}
</style>
