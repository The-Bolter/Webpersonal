<template>
  <nav class="app-nav" :class="{ scrolled: isScrolled, 'menu-open': store.isMenuOpen }">
    <div class="nav-inner">
      <a href="#hero" class="nav-museum-name" @click="scrollToSection('hero')">
        The Curator's Log
      </a>

      <!-- Desktop links -->
      <div class="nav-links-desktop">
        <a
          v-for="link in links"
          :key="link.id"
          :href="`#${link.id}`"
          class="nav-editorial-link"
          :class="{ active: store.activeSection === link.id }"
          @click.prevent="scrollToSection(link.id)"
        >{{ link.label }}</a>
      </div>

      <!-- Menu toggle -->
      <button class="menu-toggle" @click="store.toggleMenu" :aria-label="store.isMenuOpen ? 'Close' : 'Menu'">
        <span></span><span></span>
      </button>
    </div>

    <!-- Mobile menu overlay -->
    <transition name="menu-overlay">
      <div v-if="store.isMenuOpen" class="menu-overlay" @click="store.closeMenu"></div>
    </transition>

    <!-- Mobile menu panel -->
    <div class="nav-links-mobile" :class="{ active: store.isMenuOpen }">
      <a
        v-for="(link, i) in links"
        :key="link.id"
        :href="`#${link.id}`"
        class="mobile-link"
        :class="{ active: store.activeSection === link.id }"
        :style="{ transitionDelay: store.isMenuOpen ? `${0.1 + i * 0.08}s` : '0s' }"
        @click.prevent="scrollToSection(link.id)"
      >{{ link.label }}</a>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAppStore } from '../store'

const store = useAppStore()
const isScrolled = ref(false)

const links = [
  { id: 'about', label: 'Philosophy' },
  { id: 'projects', label: 'Collection' },
  { id: 'resume', label: 'Provenance' },
  { id: 'works', label: 'Archive' },
  { id: 'contact', label: 'Correspondence' }
]

function scrollToSection(id) {
  store.closeMenu()
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

function onScroll() {
  isScrolled.value = window.scrollY > 60
  const sections = document.querySelectorAll('section[id]')
  let current = 'hero'
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 150) current = s.getAttribute('id')
  })
  store.setActiveSection(current)
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.app-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  height: var(--nav-height);
  transition: background 0.6s var(--ease-out), box-shadow 0.6s var(--ease-out);
}

.app-nav.scrolled {
  background: rgba(229, 213, 189, 0.5);
  backdrop-filter: blur(4px);
  box-shadow: 0 1px 0 rgba(139, 132, 120, 0.04);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--space-xl);
}

.nav-museum-name {
  font-family: var(--font-editorial);
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  transition: color var(--dur-fast) var(--ease-out);
}

.nav-museum-name:hover { color: var(--ink-green); }

/* Desktop links */
.nav-links-desktop {
  display: flex;
  align-items: center;
  gap: 2.8rem;
}

.nav-editorial-link {
  font-family: var(--font-editorial);
  font-size: 0.95rem;
  font-weight: 400;
  color: var(--ink-light);
  letter-spacing: 0.06em;
  position: relative;
  padding: 0.2rem 0;
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out);
}

.nav-editorial-link::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0;
  width: 0;
  height: 1px;
  background: var(--ink-green);
  transition: width var(--dur-base) var(--ease-out);
}

.nav-editorial-link:hover {
  color: var(--ink-dark);
  letter-spacing: 0.09em;
}

.nav-editorial-link.active {
  color: var(--ink-dark);
}

.nav-editorial-link:hover::after,
.nav-editorial-link.active::after {
  width: 100%;
}

/* Menu toggle — two lines → X */
.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: 4px;
  z-index: 1002;
  position: relative;
  width: 24px;
  height: 18px;
  justify-content: center;
}

.menu-toggle span {
  display: block;
  width: 24px;
  height: 1.5px;
  background: var(--ink);
  transition: transform 0.5s var(--ease-out),
              opacity 0.25s ease;
  transform-origin: center;
}

.menu-open .menu-toggle span:nth-child(1) {
  transform: translateY(3px) rotate(45deg);
}

.menu-open .menu-toggle span:nth-child(2) {
  transform: translateY(-3px) rotate(-45deg);
}

/* Mobile menu overlay */
.menu-overlay {
  position: fixed;
  inset: 0;
  background: rgba(209, 187, 154, 0.3);
  backdrop-filter: blur(2px);
  z-index: 998;
}

.menu-overlay-enter-active { transition: opacity 0.5s var(--ease-out); }
.menu-overlay-leave-active { transition: opacity 0.4s var(--ease-out); }
.menu-overlay-enter-from,
.menu-overlay-leave-to { opacity: 0; }

/* Mobile menu panel */
.nav-links-mobile {
  display: none;
}

@media (max-width: 768px) {
  .nav-links-desktop { display: none; }
  .menu-toggle { display: flex; }

  .nav-links-mobile {
    display: flex;
    position: fixed;
    top: 0; right: 0;
    width: min(68vw, 260px);
    height: 100vh;
    flex-direction: column;
    justify-content: center;
    gap: 1.6rem;
    background: rgba(234, 220, 197, 0.97);
    backdrop-filter: blur(12px);
    transform: translateX(100%);
    transition: transform 0.55s cubic-bezier(0.32, 0, 0.67, 0);
    padding: var(--space-3xl);
    z-index: 999;
    box-shadow: -4px 0 32px rgba(61, 57, 45, 0.06);
  }

  .nav-links-mobile.active {
    transform: translateX(0);
    transition: transform 0.5s cubic-bezier(0.22, 0.03, 0.26, 1);
  }

  /* Staggered link reveal */
  .mobile-link {
    font-family: var(--font-editorial);
    font-size: 1.25rem;
    font-weight: 400;
    color: var(--ink);
    letter-spacing: 0.05em;
    opacity: 0;
    transform: translateX(24px);
    transition: opacity 0.5s var(--ease-out),
                transform 0.5s var(--ease-out),
                color var(--dur-fast) var(--ease-out);
    transition-delay: 0s;
  }

  .nav-links-mobile.active .mobile-link {
    opacity: 1;
    transform: translateX(0);
  }

  .mobile-link:hover,
  .mobile-link.active {
    color: var(--ink-green);
  }
}
</style>
