<template>
  <section id="projects" class="projects-section">
    <div class="container">
      <div class="projects-header ink-reveal">
        <p class="editorial-label">The Collection</p>
        <h2 class="editorial-title">
          Selected<br><em>Works</em>
        </h2>
      </div>

      <div class="collection-layout">
        <!-- Left: Featured piece — exhibition highlight -->
        <div class="featured-area ink-reveal ink-reveal-delay-1" v-if="store.featuredProject">
          <div class="featured-card museum-label">
            <span class="featured-accent"></span>
            <h3 class="featured-title">{{ store.featuredProject.title }}</h3>
            <p class="featured-desc">{{ store.featuredProject.description }}</p>
            <div class="featured-tags">
              <span v-for="tag in store.featuredProject.tags" :key="tag" class="tag-item">{{ tag }}</span>
            </div>
            <a
              v-if="store.featuredProject.github"
              :href="store.featuredProject.github"
              target="_blank"
              rel="noopener"
              class="view-link"
            >View Work &rarr;</a>
          </div>
        </div>

        <!-- Right: Secondary pieces -->
        <div class="other-pieces">
          <div
            v-for="(project, i) in store.otherProjects"
            :key="project.id"
            class="piece-card museum-label ink-reveal"
            :class="`ink-reveal-delay-${i + 2}`"
          >
            <span class="piece-index">0{{ i + 2 }}</span>
            <div class="piece-content">
              <h4>{{ project.title }}</h4>
              <p>{{ project.description }}</p>
              <span class="piece-tags">{{ project.tags.join(' / ') }}</span>
            </div>
          </div>

          <!-- Curatorial note at bottom -->
          <div class="curatorial-note ink-reveal ink-reveal-delay-4">
            <span class="note-mark">&#8258;</span>
            <p>Each piece selected for its resonance and the story it tells.</p>
            <span class="note-sign">The Curator's Log</span>
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
.projects-section {
  padding: var(--space-section) 0;
}

.projects-header {
  margin-bottom: var(--space-3xl);
}

/* Layout: asymmetric — left 5 / right 7 */
.collection-layout {
  display: grid;
  grid-template-columns: 5fr 7fr;
  gap: var(--space-3xl);
  align-items: start;
}

/* === Featured piece === */
.featured-card {
  position: relative;
  padding: var(--space-2xl) var(--space-2xl) var(--space-xl);
}

.featured-accent {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right, var(--ink-green), transparent);
  opacity: 0.3;
}

.featured-title {
  font-family: var(--font-editorial);
  font-size: 1.8rem;
  font-weight: 400;
  color: var(--ink-dark);
  letter-spacing: 0.03em;
  margin-bottom: var(--space-lg);
  line-height: 1.2;
}

.featured-desc {
  font-size: 0.95rem;
  color: var(--ink-light);
  line-height: 1.9;
  margin-bottom: var(--space-xl);
}

.featured-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: var(--space-xl);
}

.tag-item {
  font-family: var(--font-label);
  font-size: 0.65rem;
  color: var(--bark);
  border: 1px solid rgba(154, 132, 110, 0.2);
  padding: 0.2rem 0.65rem;
  border-radius: 2px;
  letter-spacing: 0.05em;
}

.view-link {
  font-family: var(--font-label);
  font-size: 0.75rem;
  color: var(--ink-green);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out);
}

.view-link:hover {
  color: var(--ink-dark);
  letter-spacing: 0.14em;
}

/* === Secondary pieces === */
.other-pieces {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.piece-card {
  display: flex;
  gap: var(--space-lg);
  align-items: flex-start;
  padding: var(--space-lg) var(--space-xl);
}

.piece-index {
  font-family: var(--font-editorial);
  font-size: 0.85rem;
  color: var(--bark-light);
  letter-spacing: 0.04em;
  flex-shrink: 0;
  padding-top: 2px;
}

.piece-content { flex: 1; min-width: 0; }

.piece-content h4 {
  font-family: var(--font-editorial);
  font-size: 1.15rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin-bottom: var(--space-xs);
}

.piece-content p {
  font-size: 0.84rem;
  color: var(--ink-light);
  line-height: 1.75;
  margin-bottom: var(--space-sm);
}

.piece-tags {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--bark);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* === Curatorial note === */
.curatorial-note {
  padding: var(--space-xl) var(--space-lg);
  border-left: 2px solid rgba(154, 132, 110, 0.15);
  max-width: 320px;
}

.note-mark {
  font-size: 1.2rem;
  color: var(--bark-light);
  display: block;
  margin-bottom: var(--space-sm);
}

.curatorial-note p {
  font-family: var(--font-editorial);
  font-size: 0.95rem;
  color: var(--ink);
  line-height: 1.7;
  margin-bottom: var(--space-sm);
}

.note-sign {
  font-family: var(--font-label);
  font-size: 0.6rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

@media (max-width: 768px) {
  .collection-layout { grid-template-columns: 1fr; gap: var(--space-2xl); }
  .featured-title { font-size: 1.5rem; }
  .piece-card { flex-direction: column; gap: var(--space-sm); }
  .curatorial-note { max-width: 100%; }
}
</style>
