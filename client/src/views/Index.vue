<template>
  <div class="index-page">
    <!-- Fixed landscape scene (always visible) -->
    <div class="scene">
      <ConceptArtLayer />
      <WaterMotionLayer />
      <WaterRippleLayer />
      <PlumBranchLayer />

      <!-- Soft fog behind content (no visible boundary) -->
      <div class="content-haze" aria-hidden="true"></div>

      <!-- Intro guide -->
      <transition name="guide-fade">
        <p v-if="showGuide" class="intro-guide">Follow the blossoms</p>
      </transition>

      <!-- Floating content (no container) -->
      <div class="sheet-anchor">
        <div ref="sheetRef" class="content-sheet">
          <div class="sheet-scroll">
            <transition name="sheet" mode="out-in">
              <component :is="sheets[activeIndex]" :key="activeIndex" @next="handleNext" />
            </transition>
          </div>
        </div>

        <!-- State navigation (states 1+, directly below content) -->
        <button v-if="activeIndex > 0" class="state-nav" @click="handleNext" :aria-label="isLast ? '返回顶部' : '继续了解'">
          <span class="state-nav-text">{{ isLast ? '返回' : '继续了解' }}</span>
          <span class="state-nav-arrow">{{ isLast ? '↑' : '→' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import ConceptArtLayer from '../components/ConceptArtLayer.vue'
import PlumBranchLayer from '../components/PlumBranchLayer.vue'
import WaterMotionLayer from '../components/WaterMotionLayer.vue'
import WaterRippleLayer from '../components/WaterRippleLayer.vue'
import IndexHeroContent from '../components/index/IndexHeroContent.vue'
import IndexCapabilities from '../components/index/IndexCapabilities.vue'
import IndexProjects from '../components/index/IndexProjects.vue'
import IndexJourney from '../components/index/IndexJourney.vue'
import IndexStudio from '../components/index/IndexStudio.vue'
import IndexAbout from '../components/index/IndexAbout.vue'
import IndexContact from '../components/index/IndexContact.vue'
import { useAppStore } from '../store'

const store = useAppStore()
const activeIndex = ref(0)
const sheetRef = ref(null)
const showGuide = ref(false)
let guideShown = false
let guideTimers = []

const sheets = [
  IndexHeroContent,
  IndexCapabilities,
  IndexProjects,
  IndexJourney,
  IndexStudio,
  IndexAbout,
  IndexContact
]

const totalStates = sheets.length
const isLast = computed(() => activeIndex.value === totalStates - 1)

function handleNext() {
  activeIndex.value = activeIndex.value + 1 >= totalStates ? 0 : activeIndex.value + 1
}

onMounted(() => {
  // Content entrance — fade in + slight rise, then stays stable
  if (sheetRef.value) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!reduceMotion) {
      gsap.fromTo(
        sheetRef.value,
        { opacity: 0, y: 16 },
        { opacity: 1, y: 0, duration: 1.1, ease: 'power2.out', delay: store.isLoading ? 5 : 0.3 }
      )
    }
  }

  // First-visit intro guide (once per session)
  if (sessionStorage.getItem('plum_guide_seen')) return
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return

  const wait = store.isLoading ? 6000 : 1500
  guideTimers.push(setTimeout(() => {
    guideShown = true
    store.setHovered('projects')
    showGuide.value = true
    sessionStorage.setItem('plum_guide_seen', '1')
    guideTimers.push(setTimeout(() => {
      showGuide.value = false
      store.clearHovered()
      guideShown = false
    }, 4500))
  }, wait))
})

watch(
  () => store.hoveredId,
  () => {
    if (guideShown && showGuide.value) {
      showGuide.value = false
    }
  }
)

onUnmounted(() => {
  guideTimers.forEach(t => clearTimeout(t))
})
</script>

<style scoped>
.index-page {
  position: relative;
  min-height: 100vh;
}

.scene {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

/* Soft fog behind content — radial, no visible boundary */
.content-haze {
  position: fixed;
  left: 28%;
  top: 55%;
  transform: translate(-50%, -50%);
  width: 68vw;
  height: 64vh;
  background: radial-gradient(ellipse at center, rgba(252, 247, 238, 0.42) 0%, rgba(252, 247, 238, 0.18) 45%, transparent 75%);
  z-index: 0;
  pointer-events: none;
}

.intro-guide {
  position: absolute;
  top: calc(var(--nav-height) + var(--space-lg));
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  margin: 0;
  font-family: var(--font-label);
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--ink-green);
  pointer-events: none;
}

.guide-fade-enter-active,
.guide-fade-leave-active {
  transition: opacity 1.2s var(--ease-out);
}
.guide-fade-enter-from,
.guide-fade-leave-to {
  opacity: 0;
}

/* Content — floats directly on the landscape, no card container */
.sheet-anchor {
  position: absolute;
  left: 38%;
  top: 55%;
  transform: translate(-50%, -50%);
  width: min(54vw, 760px);
  pointer-events: auto;
  z-index: 1;
  text-align: center;
}

.content-sheet {
  position: relative;
  width: 100%;
  padding: var(--space-xl) 0;
}

.sheet-scroll {
  max-height: 46vh;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.sheet-scroll::-webkit-scrollbar {
  width: 4px;
}
.sheet-scroll::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.22);
  border-radius: 2px;
}

/* Content transition: leave up, enter from below */
.sheet-enter-active,
.sheet-leave-active {
  transition: opacity 0.55s var(--ease-out), transform 0.55s var(--ease-out);
}
.sheet-enter-from {
  opacity: 0;
  transform: translateY(16px);
}
.sheet-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}

/* State navigation — directly below content */
.state-nav {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  pointer-events: auto;
  z-index: 3;
  margin-top: var(--space-lg);
  padding: 0.4rem 0.8rem;
}

.state-nav-text {
  font-family: var(--font-label);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--ink);
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.7);
  transition: color var(--dur-fast) var(--ease-out);
}

.state-nav-arrow {
  font-size: 0.85rem;
  color: var(--bark);
  transition: transform var(--dur-fast) var(--ease-out);
}

.state-nav:hover .state-nav-text {
  color: var(--ink-dark);
}

.state-nav:hover .state-nav-arrow {
  transform: translateX(3px);
}

@media (max-width: 1024px) {
  .sheet-anchor {
    width: min(64vw, 640px);
  }
}

@media (max-width: 768px) {
  .sheet-anchor {
    left: 50%;
    top: 52%;
    width: 88vw;
  }
  .sheet-scroll {
    max-height: 54vh;
  }
  .content-haze {
    left: 50%;
    top: 52%;
    width: 90vw;
    height: 60vh;
  }
}
</style>
