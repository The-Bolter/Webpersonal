<template>
  <div ref="pageRef" class="studio-page" data-lenis-prevent>
    <!-- Fixed landscape background -->
    <div class="page-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" />
    </div>

    <!-- Subtle readability veil -->
    <div class="page-veil" aria-hidden="true"></div>

    <!-- Window mask: clips content to the painted window interior -->
    <div ref="maskRef" class="studio-window-mask">
      <div class="studio-scroll-area" data-lenis-prevent>
        <div class="studio-content">
          <WorksSection />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import bgSrc from '../assets/pages/studio-bg.png'
import WorksSection from '../components/WorksSection.vue'
import { useInkReveal } from '../composables/useInkReveal'

useInkReveal()

const pageRef = ref(null)
const maskRef = ref(null)

// Painted window interior, as fractions of the background image (1672x941).
// Measured from the frame bars: left col ~9.6%, right col ~91.6%,
// top row ~2.9%, bottom row ~86.8%.
const IMG_W = 1672
const IMG_H = 941
const WINDOW = { left: 0.096, top: 0.029, right: 0.916, bottom: 0.868 }

function computeWindow() {
  const page = pageRef.value
  const mask = maskRef.value
  if (!page || !mask) return

  const pw = page.clientWidth
  const ph = page.clientHeight
  if (!pw || !ph) return

  // Same math as object-fit: cover (center)
  const scale = Math.max(pw / IMG_W, ph / IMG_H)
  const dispW = IMG_W * scale
  const dispH = IMG_H * scale
  const offX = (pw - dispW) / 2
  const offY = (ph - dispH) / 2

  let left = offX + WINDOW.left * dispW
  let top = offY + WINDOW.top * dispH
  let right = offX + WINDOW.right * dispW
  let bottom = offY + WINDOW.bottom * dispH

  // Clip to the page bounds (window may be partially cropped by cover)
  left = Math.max(0, left)
  top = Math.max(0, top)
  right = Math.min(pw, right)
  bottom = Math.min(ph, bottom)

  mask.style.left = left + 'px'
  mask.style.top = top + 'px'
  mask.style.width = (right - left) + 'px'
  mask.style.height = (bottom - top) + 'px'
}

onMounted(() => {
  computeWindow()
  window.addEventListener('resize', computeWindow)
  // Lock page-level vertical scroll only while /studio is active
  document.documentElement.classList.add('studio-page-active')
  document.body.classList.add('studio-page-active')
})

onUnmounted(() => {
  window.removeEventListener('resize', computeWindow)
  document.documentElement.classList.remove('studio-page-active')
  document.body.classList.remove('studio-page-active')
})
</script>

<style scoped>
.studio-page {
  position: relative;
  height: 100dvh;
  min-height: 0;
  overflow: hidden;
}

.page-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.page-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.page-veil {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: rgba(245, 236, 222, 0.28);
}

/* Window mask — clips content to the painted window interior only */
.studio-window-mask {
  position: absolute;
  z-index: 1;
  overflow: hidden;
  pointer-events: auto;
  /* Fallback for first paint (16:9 viewport); corrected by JS on mount */
  left: 9.6%;
  top: 2.9%;
  width: 82%;
  height: 83.9%;
}

.studio-scroll-area {
  width: 100%;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.studio-content {
  height: auto;
  min-height: max-content;
  padding-top: var(--space-xl);
  padding-bottom: var(--space-xl);
}

.studio-scroll-area::-webkit-scrollbar {
  width: 4px;
}
.studio-scroll-area::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.25);
  border-radius: 2px;
}
</style>
