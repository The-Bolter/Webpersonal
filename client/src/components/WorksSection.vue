<template>
  <section id="works" class="works-section">
    <div class="container">
      <div class="works-header ink-reveal">
        <p class="editorial-label">The Archive</p>
        <h2 class="editorial-title">
          Curated<br><em>Studies</em>
        </h2>
      </div>

      <!-- Filters -->
      <div class="archive-filters ink-reveal ink-reveal-delay-1">
        <button
          v-for="filter in filters"
          :key="filter.value"
          class="filter-link"
          :class="{ active: store.workFilter === filter.value }"
          @click="store.workFilter = filter.value"
        >
          {{ filter.label }}
          <span class="filter-count" v-if="filter.value === 'all'">({{ store.works.length }})</span>
        </button>
      </div>

      <!-- Archive grid -->
      <div class="archive-grid">
        <div
          v-for="(work, i) in store.filteredWorks"
          :key="work.id"
          class="ink-reveal"
          :class="`ink-reveal-delay-${(i % 3) + 1}`"
        >
          <div class="archive-card museum-label">
            <!-- Category indicator -->
            <div class="archive-card-top">
              <span class="archive-cat-dot" :class="`cat-${work.category}`"></span>
              <span class="archive-category">{{ work.category }}</span>
            </div>

            <h4>{{ work.title }}</h4>
            <p class="archive-desc">{{ work.description }}</p>

            <div class="archive-card-foot">
              <a v-if="work.link" :href="work.link" target="_blank" rel="noopener" class="archive-link">
                View Study &rarr;
              </a>
              <span v-else class="archive-unlinked">Internal Archive</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="store.filteredWorks.length === 0" class="archive-empty ink-reveal">
        <p>No entries under this category yet.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useAppStore } from '../store'
const store = useAppStore()

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Code', value: 'code' },
  { label: 'Design', value: 'design' },
  { label: 'AI', value: 'ai' }
]
</script>

<style scoped>
.works-section {
  padding: var(--space-section) 0;
}

.works-header {
  margin-bottom: var(--space-3xl);
}

/* Filters */
.archive-filters {
  display: flex;
  gap: var(--space-2xl);
  margin-bottom: var(--space-3xl);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid rgba(154, 132, 110, 0.12);
}

.filter-link {
  font-family: var(--font-editorial);
  font-size: 1rem;
  color: var(--ink-light);
  letter-spacing: 0.05em;
  padding-bottom: 2px;
  border-bottom: 1px solid transparent;
  transition: color var(--dur-fast) var(--ease-out),
              border-color var(--dur-fast) var(--ease-out);
  display: inline-flex;
  align-items: baseline;
  gap: 0.25rem;
}

.filter-link:hover { color: var(--ink-dark); }

.filter-link.active {
  color: var(--ink-dark);
  border-bottom-color: var(--ink-green);
}

.filter-count {
  font-size: 0.7rem;
  color: var(--bark);
}

/* Grid */
.archive-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-xl) var(--space-2xl);
}

/* Card */
.archive-card {
  padding: var(--space-xl) var(--space-xl) var(--space-lg);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.archive-card-top {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.archive-cat-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.cat-code    { background: #8d7d68; }
.cat-design  { background: #b8a48e; }
.cat-ai      { background: #6b5a48; }

.archive-category {
  font-family: var(--font-label);
  font-size: 0.6rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

.archive-card h4 {
  font-family: var(--font-editorial);
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin-bottom: var(--space-sm);
  line-height: 1.3;
}

.archive-desc {
  font-size: 0.85rem;
  color: var(--ink-light);
  line-height: 1.8;
  margin-bottom: var(--space-lg);
  flex: 1;
}

.archive-card-foot {
  padding-top: var(--space-md);
  border-top: 1px solid rgba(154, 132, 110, 0.08);
}

.archive-link {
  font-family: var(--font-label);
  font-size: 0.7rem;
  color: var(--ink-green);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  transition: letter-spacing var(--dur-base) var(--ease-out),
              color var(--dur-fast) var(--ease-out);
}

.archive-link:hover {
  letter-spacing: 0.13em;
  color: var(--ink-dark);
}

.archive-unlinked {
  font-family: var(--font-label);
  font-size: 0.65rem;
  color: var(--bark-light);
  letter-spacing: 0.06em;
}

/* Empty state */
.archive-empty {
  text-align: center;
  padding: var(--space-3xl) 0;
}

.archive-empty p {
  font-family: var(--font-editorial);
  font-size: 1.05rem;
  color: var(--bark);
}

@media (max-width: 768px) {
  .archive-grid { grid-template-columns: 1fr; gap: var(--space-lg); }
  .archive-filters { gap: var(--space-lg); flex-wrap: wrap; border-bottom: none; }
}
</style>
