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

      <!-- Floating content (no container) -->
      <div class="sheet-anchor">
        <div ref="sheetRef" class="content-sheet">
          <div class="sheet-scroll">
            <transition name="sheet" mode="out-in">
              <component :is="sheets[activeIndex]" :key="activeIndex" @next="goNext" />
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
  activeIndex.value = (activeIndex.value + 1) % totalStates
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
