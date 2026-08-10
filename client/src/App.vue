<template>
  <div class="app-wrapper">
    <BackgroundCanvas />
    <LoadingScreen />
    <AppNav />
    <main>
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
    <ScrollToTop />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from './store'
import { useLenis } from './composables/useLenis'
import BackgroundCanvas from './components/BackgroundCanvas.vue'
import AppNav from './components/AppNav.vue'
import AppFooter from './components/AppFooter.vue'
import LoadingScreen from './components/LoadingScreen.vue'
import ScrollToTop from './components/ScrollToTop.vue'

const store = useAppStore()

// Initialize Lenis smooth scroll
useLenis()

onMounted(() => {
  setTimeout(() => store.finishLoading(), 1800)
})
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.8s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

.app-wrapper {
  position: relative;
  min-height: 100vh;
}

main {
  position: relative;
  z-index: 1;
}
</style>
