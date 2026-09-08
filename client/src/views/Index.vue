<template>
  <div class="index-page">
    <!-- Fixed landscape scene (always visible) -->
    <div class="scene">
      <div class="scene-visuals" :class="{ 'is-ready': visualGroupReady }">
        <ConceptArtLayer />
        <WaterMotionLayer />
        <WaterRippleLayer />
        <PlumBranchLayer @guide-done="onGuideDone" />
        <PetalCanvas ref="petalRef" />
      </div>

      <!-- Soft fog behind content (no visible boundary) -->
      <div class="content-haze" aria-hidden="true"></div>

      <!-- Floating content (no container) -->
      <div class="sheet-anchor">
        <div ref="sheetRef" class="content-sheet">
          <div class="sheet-scroll">
            <transition name="sheet" mode="out-in">
              <component :is="sheets[activeIndex]" :key="activeIndex" @next="goNext" />
            </transition>
          </div>

          <nav v-if="activeIndex > 0" class="sheet-nav" aria-label="内容浏览">
            <button class="sheet-nav-link" @click="goBack" aria-label="返回">← 返回</button>
            <button
              v-if="activeIndex < totalStates - 1"
              class="sheet-nav-link"
              @click="goNext"
              aria-label="继续了解"
            >继续了解 →</button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, onActivated, onDeactivated } from 'vue'
import gsap from 'gsap'
import ConceptArtLayer from '../components/ConceptArtLayer.vue'
import PlumBranchLayer from '../components/PlumBranchLayer.vue'
import PetalCanvas from '../components/PetalCanvas.vue'
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
import { waitForVisualGroup } from '../composables/useVisualPreload'
import conceptSrc from '../assets/index/concept/index-v1-concept.lossless.webp'
import plumSrc from '../assets/index/plum/plum-branch.lossless.webp'

const store = useAppStore()
const activeIndex = ref(0)
const sheetRef = ref(null)
const petalRef = ref(null)
const visualGroupReady = ref(false)
let isActive = true
let idleHandle = null
let cancelIdle = null
let petalsStarted = false
let petalsStarting = false
let petalFallbackTimer = null

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

function goNext() {
  activeIndex.value = Math.min(activeIndex.value + 1, totalStates - 1)
}

function goBack() {
  activeIndex.value = Math.max(activeIndex.value - 1, 0)
}

function onGuideDone(detail) {
  ensurePetalsStarted(detail || { skipped: false })
}

async function ensurePetalsStarted(detail = { skipped: true }) {
  if (petalsStarted || petalsStarting || !petalRef.value) return
  petalsStarting = true
  try {
    const started = await petalRef.value.start(detail)
    if (started) petalsStarted = true
  } finally {
    petalsStarting = false
  }
}

watch(visualGroupReady, (ready) => {
  if (ready) ensurePetalsStarted()
})

onMounted(() => {
  waitForVisualGroup([conceptSrc, plumSrc], 1800)
    .then(() => {
      if (!isActive) return
      visualGroupReady.value = true
      const warmRoutes = () => {
        if (!isActive) return
        // Warm only the two most likely next route chunks after the first
        // scene is ready; their images remain unrequested until route entry.
        import('../views/Projects.vue')
        import('../views/Journey.vue')
      }
      if ('requestIdleCallback' in window) {
        idleHandle = window.requestIdleCallback(warmRoutes, { timeout: 2000 })
        cancelIdle = () => window.cancelIdleCallback(idleHandle)
      } else {
        idleHandle = window.setTimeout(warmRoutes, 1800)
        cancelIdle = () => window.clearTimeout(idleHandle)
      }
    })
  petalFallbackTimer = window.setTimeout(() => {
    ensurePetalsStarted({ skipped: true })
  }, 2000)
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
})

onUnmounted(() => {
  isActive = false
  if (petalFallbackTimer) window.clearTimeout(petalFallbackTimer)
  petalRef.value?.stop()
  petalsStarted = false
  petalsStarting = false
  if (cancelIdle) cancelIdle()
})

onActivated(() => {
  ensurePetalsStarted({ skipped: true })
})

onDeactivated(() => {
  if (petalFallbackTimer) window.clearTimeout(petalFallbackTimer)
  petalRef.value?.stop()
  petalsStarted = false
  petalsStarting = false
})
</script>

<style scoped>
.index-page {
  position: relative;
  min-height: 100dvh;
}

.scene {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.scene-visuals {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.55s ease;
}

.scene-visuals.is-ready { opacity: 1; }

/* Soft fog behind content — radial, no visible boundary */
.content-haze {
  position: absolute;
  left: 28%;
  top: 55%;
  transform: translate(-50%, -50%);
  width: 68vw;
  height: 64vh;
  background: radial-gradient(ellipse at center, rgba(252, 247, 238, 0.42) 0%, rgba(252, 247, 238, 0.18) 45%, transparent 75%);
  z-index: 0;
  pointer-events: none;
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

/* Reading navigation — follows content height, no card, no fixed Y */
.sheet-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: clamp(20px, 3vh, 40px);
}

.sheet-nav-link {
  background: none;
  border: none;
  padding: 0.3rem 0;
  cursor: pointer;
  font-family: var(--font-label);
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  color: var(--ink);
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.7);
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out);
}

.sheet-nav-link:hover {
  color: var(--ink-dark);
  letter-spacing: 0.22em;
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
