<template>
  <footer class="app-footer">
    <div class="container footer-top">
      <div class="footer-motto">
        <p>Building digital experiences that feel as personal and considered as a handwritten note.</p>
      </div>

      <div class="footer-links">
        <div class="footer-group">
          <p class="footer-group-label">The Atelier</p>
          <a href="#about" @click.prevent="scrollTo('about')">Philosophy</a>
          <a href="#projects" @click.prevent="scrollTo('projects')">Collection</a>
          <a href="#works" @click.prevent="scrollTo('works')">Archive</a>
        </div>

        <div class="footer-group">
          <p class="footer-group-label">Connect</p>
          <a :href="`mailto:${store.profile.social.email}`">Correspondence</a>
          <a :href="store.profile.social.github" target="_blank" rel="noopener">Studio</a>
          <a :href="store.profile.social.linkedin" target="_blank" rel="noopener">Network</a>
        </div>
      </div>
    </div>

    <div class="footer-bottom container">
      <p>&copy; {{ year }} {{ store.profile.name }} &mdash; Made with care and contemplation.</p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '../store'

const store = useAppStore()
const year = computed(() => new Date().getFullYear())

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.app-footer {
  background: var(--paper-dark);
  border-top: 1px solid rgba(139, 132, 120, 0.1);
  padding: var(--space-3xl) 0 var(--space-xl);
  position: relative;
  z-index: 1;
}

.footer-top {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: var(--space-3xl);
  margin-bottom: var(--space-3xl);
}

.footer-motto p {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--ink-light);
  line-height: 1.85;
  max-width: 320px;
  margin: 0;
}

.footer-links {
  display: flex;
  gap: var(--space-3xl);
}

.footer-group-label {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: var(--space-lg);
}

.footer-group a {
  display: block;
  font-family: var(--font-editorial);
  font-size: 0.9rem;
  color: var(--ink-light);
  padding: 0.25rem 0;
  letter-spacing: 0.04em;
  transition: color var(--dur-fast) var(--ease-out);
}

.footer-group a:hover { color: var(--ink-dark); }

.footer-bottom {
  text-align: center;
  padding-top: var(--space-xl);
  border-top: 1px solid rgba(139, 132, 120, 0.1);
}

.footer-bottom p {
  font-family: var(--font-label);
  font-size: 0.68rem;
  color: var(--ink-light);
  letter-spacing: 0.04em;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-top { grid-template-columns: 1fr; gap: var(--space-2xl); }
  .footer-links { gap: var(--space-2xl); }
}
</style>
