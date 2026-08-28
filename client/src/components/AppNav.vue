<template>
  <nav class="app-nav" :class="{ 'menu-open': store.isMenuOpen }">
    <div class="nav-inner">
      <router-link to="/" class="nav-logo" @click="store.closeMenu">
        <img
          src="@/assets/images/branding/catherinesstudio.png"
          alt="Catherine's Studio"
        />
      </router-link>

      <!-- Desktop links -->
      <div class="nav-links-desktop">
        <router-link
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="nav-editorial-link"
          :class="{ active: $route.path === link.to, synced: link.key && store.hoveredId === link.key }"
          @click="store.closeMenu"
          @mouseenter="link.key && store.setHovered(link.key)"
          @mouseleave="store.clearHovered"
        >
          <span class="nav-label-en">{{ link.en }}</span>
          <span class="nav-label-cn">{{ link.cn }}</span>
        </router-link>
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
      <router-link
        v-for="(link, i) in links"
        :key="link.to"
        :to="link.to"
        class="mobile-link"
        :class="{ active: $route.path === link.to }"
        :style="{ transitionDelay: store.isMenuOpen ? `${0.1 + i * 0.08}s` : '0s' }"
        @click="store.closeMenu"
      >
        <span class="nav-label-en">{{ link.en }}</span>
        <span class="nav-label-cn">{{ link.cn }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useAppStore } from '../store'

const store = useAppStore()

const links = [
  { to: '/', en: 'INDEX', cn: '首页', key: null },
  { to: '/projects', en: 'PROJECTS', cn: '项目档案', key: 'projects' },
  { to: '/journey', en: 'JOURNEY', cn: '成长轨迹', key: 'journey' },
  { to: '/studio', en: 'STUDIO', cn: '创意档案', key: 'studio' },
  { to: '/about', en: 'ABOUT', cn: '关于我', key: 'about' },
  { to: '/contact', en: 'CONTACT', cn: '建立连接', key: 'contact' }
]
</script>

<style scoped>
.app-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  height: var(--nav-height);
  margin-bottom: calc(-1 * var(--nav-height));
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  width: 100%;
  padding: 0 clamp(var(--space-lg), 4vw, var(--space-2xl));
}

.nav-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;
}

.nav-logo img {
  width: clamp(180px, 24vw, 420px);
  height: auto;
  display: block;
  margin-top: 15px;
}

/* Desktop links */
.nav-links-desktop {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  gap: var(--space-md);
  flex: 1 1 auto;
  min-width: max-content;
  flex-shrink: 0;
  padding-left: var(--space-xl);
}

.nav-editorial-link {
  font-family: var(--font-editorial);
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--ink-light);
  letter-spacing: 0.08em;
  position: relative;
  padding: 0.2rem 0;
  text-decoration: none;
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out);
  display: flex;
  flex-direction: row;
  white-space: nowrap;
  align-items: baseline;
  gap: 6px;
  flex-shrink: 0;
}

.nav-label-cn {
  font-family: var(--font-label);
  font-size: 0.7rem;
  color: var(--bark);
  letter-spacing: 0.12em;
  text-transform: none;
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
  letter-spacing: 0.11em;
}

.nav-editorial-link.active {
  color: var(--ink-dark);
}

.nav-editorial-link:hover::after,
.nav-editorial-link.active::after {
  width: 100%;
}

.nav-editorial-link.synced {
  color: var(--ink-dark);
}

.nav-editorial-link.synced .nav-label-en {
  opacity: 1;
}

.nav-editorial-link.synced::after {
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
</style>
