<template>
  <div class="plum-layer">
    <div ref="recoilRef" class="plum-recoil">
      <div ref="wrapperRef" class="plum-wrapper">
        <div ref="innerRef" class="plum-inner">
          <img :src="plumSrc" alt="" class="plum-image" />

          <div
            v-for="f in flowers"
            :key="f.id"
            :ref="el => setFlowerEl(el, f.id)"
            class="flower"
            :class="[f.id, { synced: store.hoveredId === f.id, guided: guidedId === f.id }]"
            :style="{ left: f.x + '%', top: f.y + '%' }"
            @mouseenter="onFlowerEnter(f)"
            @mouseleave="store.clearHovered"
            @click="onFlowerClick(f)"
          >
            <span class="flower-core" :ref="el => setCoreRef(el, f.id)">
              <span class="flower-halo"></span>
              <span class="hotspot-label">{{ f.label }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <FlowerPetalLayer ref="petalLayerRef" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import plumSrc from '../assets/index/plum/plum-branch.png'
import { useAppStore } from '../store'
import FlowerPetalLayer from './FlowerPetalLayer.vue'

const store = useAppStore()
const router = useRouter()
const recoilRef = ref(null)
const wrapperRef = ref(null)
const innerRef = ref(null)
const petalLayerRef = ref(null)
const guidedId = ref(null)
let windTl = null
let driftTl = null
let guideTl = null
const guideActive = ref(false)
let debugTimer = null
const coreRefs = {}
const flowerEls = {}

const flowers = [
  { id: 'projects', label: 'PROJECTS', x: 48.7, y: 29.9, rx: 30, ry: 82, to: '/projects' },
  { id: 'journey', label: 'JOURNEY', x: 29.0, y: 63.0, rx: 42, ry: 86, to: '/journey' },
  { id: 'studio', label: 'STUDIO', x: 20.4, y: 54.8, rx: 54, ry: 83, to: '/studio' },
  { id: 'about', label: 'ABOUT', x: 52.8, y: 67.0, rx: 66, ry: 87, to: '/about' },
  { id: 'contact', label: 'CONTACT', x: 78.0, y: 25.9, rx: 78, ry: 81, to: '/contact' }
]

const GUIDE_ORDER = ['projects', 'journey', 'studio', 'about', 'contact']

// Debug flag — this round only (single-point origin calibration)
const DEBUG_PETAL_ORIGIN = true

function setCoreRef(el, id) {
  if (el) coreRefs[id] = el
}

function setFlowerEl(el, id) {
  if (el) flowerEls[id] = el
}

function onFlowerEnter(f) {
  stopGuide()
  store.setHovered(f.id)
  store.triggerRipple(f.id, f.rx, f.ry, 0.6)
}

function onFlowerClick(f) {
  stopGuide()
  const core = coreRefs[f.id]
  if (core) {
    gsap.timeline()
      .to(core, { scale: 1.1, rotation: 3, duration: 0.25, ease: 'power2.out' })
      .to(core, { scale: 1, rotation: 0, duration: 0.9, ease: 'sine.inOut' })
  }
  // Whole-branch recoil (separate layer, no conflict with wind)
  if (recoilRef.value) {
    gsap.timeline()
      .to(recoilRef.value, { x: 3, y: 1, rotation: 0.4, duration: 0.3, ease: 'power2.out' })
      .to(recoilRef.value, { x: 0, y: 0, rotation: 0, duration: 1.4, ease: 'sine.inOut' })
  }
  // Stronger ripple
  store.triggerRipple(f.id, f.rx, f.ry, 1.6)
  // Navigate after brief feedback
  setTimeout(() => router.push(f.to), 450)
}

function startGuide() {
  const debug = new URLSearchParams(window.location.search).has('debug-guide')
  if (!debug && sessionStorage.getItem('index_flower_guide_seen')) return
  if (!debug) sessionStorage.setItem('index_flower_guide_seen', '1')

  guideActive.value = true

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) {
    guideActive.value = false
    return
  }

  guideTl = gsap.timeline({
    onComplete: () => {
      guideActive.value = false
      guidedId.value = null
      store.clearHovered()
    }
  })

  GUIDE_ORDER.forEach((id, i) => {
    const t = i * 0.95
    guideTl.add(() => {
      guidedId.value = id
      store.setHovered(id)
      const core = coreRefs[id]
      if (core) {
        gsap.to(core, { scale: 1.1, duration: 0.2, ease: 'sine.inOut', yoyo: true, repeat: 1 })
      }
    }, t)
    guideTl.add(() => {
      guidedId.value = null
      store.clearHovered()
    }, t + 0.65)
  })

  guideTl.play()
}

function stopGuide() {
  if (guideTl) {
    guideTl.kill()
    guideTl = null
  }
  guidedId.value = null
  if (guideActive.value) {
    guideActive.value = false
    store.clearHovered()
  }
}

// Start the sequential guide once the loading screen finishes
watch(
  () => store.isLoading,
  (loading) => {
    if (!loading && !guideActive) {
      setTimeout(() => startGuide(), 350)
    }
  },
  { immediate: true }
)

// ---- Ambient petal scheduler (debug: single-petal verification) ----
function runDebugPetal() {
  if (guideActive.value) return
  const el = flowerEls.projects
  if (!el) return
  const r = el.getBoundingClientRect()
  const screenX = r.left + r.width / 2
  const screenY = r.top + r.height / 2
  petalLayerRef.value?.showOriginMarker(screenX, screenY)
  petalLayerRef.value?.spawnDebugPetal(screenX, screenY)
}

function stopDebug() {
  if (debugTimer) { debugTimer.kill(); debugTimer = null }
}

// single debug petal 800ms after loading completes (verification mode only)
watch(
  () => store.isLoading,
  (loading) => {
    if (!loading) {
      debugTimer = gsap.delayedCall(0.8, () => runDebugPetal())
    }
  }
)

onMounted(() => {
  const el = wrapperRef.value
  const inner = innerRef.value
  if (!el || !inner) return

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return

  // Wind — outer sway (pivot at root, top-right)
  windTl = gsap.timeline({
    delay: 0.5,
    repeat: -1,
    repeatDelay: 1,
    defaults: { ease: 'sine.inOut' }
  })
    .to(el, { rotation: 0.9, x: 4, y: -2, duration: 3.0 })
    .to(el, { duration: 0.6 })
    .to(el, { rotation: 0, x: 0, y: 0, duration: 3.0 })
    .to(el, { duration: 1.0 })
    .to(el, { rotation: -0.8, x: -4, y: 2, duration: 2.4 })
    .to(el, { duration: 0.5 })
    .to(el, { rotation: 0, x: 0, y: 0, duration: 2.6 })

  // Drift — secondary layer, not synchronized
  driftTl = gsap.timeline({
    delay: 0.8,
    repeat: -1,
    repeatDelay: 1.1,
    defaults: { ease: 'sine.inOut' }
  })
    .to(inner, { rotation: 0.6, x: 4, y: 2, duration: 2.6 })
    .to(inner, { duration: 0.5 })
    .to(inner, { rotation: 0, x: 0, y: 0, duration: 2.6 })
    .to(inner, { duration: 1.1 })
    .to(inner, { rotation: -0.5, x: -4, y: -2, duration: 2.0 })
    .to(inner, { duration: 0.5 })
    .to(inner, { rotation: 0, x: 0, y: 0, duration: 2.2 })
})

onUnmounted(() => {
  if (windTl) windTl.kill()
  if (driftTl) driftTl.kill()
  if (guideTl) guideTl.kill()
  stopDebug()
  petalLayerRef.value?.clearAll()
})
</script>

<style scoped>
.plum-layer {
  position: absolute;
  top: -0.9%;
  right: 0;
  width: 45%;
  max-width: 900px;
  z-index: 1;
  pointer-events: none;
}

.plum-recoil {
  width: 100%;
}

.plum-wrapper {
  width: 100%;
  transform-origin: 90% 12%;
  will-change: transform;
}

.plum-inner {
  position: relative;
  transform-origin: 85% 15%;
  will-change: transform;
}

.plum-image {
  width: 100%;
  height: auto;
  display: block;
}

/* ---- Flowers ---- */
.flower {
  position: absolute;
  width: 46px;
  height: 46px;
  margin-left: -23px;
  margin-top: -23px;
  pointer-events: auto;
  cursor: pointer;
  z-index: 2;
}

/* Per-flower idle life — extremely subtle, offset rhythms */
.flower.projects { animation: idle-breathe 7s ease-in-out infinite; }
.flower.journey { animation: idle-float 8.5s ease-in-out infinite; }
.flower.studio { animation: idle-sway 9.5s ease-in-out infinite; }
.flower.about { animation: idle-breathe-slow 11s ease-in-out infinite; }
.flower.contact { animation: idle-drift 6.5s ease-in-out infinite; }

@keyframes idle-breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.025); }
}
@keyframes idle-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}
@keyframes idle-sway {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(1deg); }
}
@keyframes idle-breathe-slow {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
@keyframes idle-drift {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(1px, -1px); }
}

.flower-core {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
}

.flower-halo {
  position: absolute;
  inset: -20px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 222, 196, 0.55) 0%, rgba(255, 222, 196, 0.16) 48%, transparent 72%);
  opacity: 0.16;
  transition: opacity 0.5s var(--ease-out);
  pointer-events: none;
}

/* Idle life — different rhythm per flower (halo) */
.flower.projects .flower-halo { animation: breathe 7s ease-in-out infinite; }
.flower.journey .flower-halo { animation: sway 9s ease-in-out infinite; }
.flower.studio .flower-halo { animation: float 8.5s ease-in-out infinite; }
.flower.about .flower-halo { animation: tremble 11s ease-in-out infinite; }
.flower.contact .flower-halo { animation: drift 6.5s ease-in-out infinite; }

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.14); }
}
@keyframes sway {
  0%, 100% { transform: rotate(-2.5deg) scale(1); }
  50% { transform: rotate(2.5deg) scale(1.08); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
@keyframes tremble {
  0%, 86%, 100% { transform: scale(1); }
  88% { transform: scale(1.06); }
  92% { transform: scale(0.98); }
  96% { transform: scale(1.03); }
}
@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(2px, -2px) scale(1.1); }
}

/* Hover / synced / guided state */
.flower:hover .flower-halo,
.flower.synced .flower-halo,
.flower.guided .flower-halo {
  opacity: 0.5;
}

.hotspot-label {
  position: absolute;
  bottom: calc(100% + 10px);
  left: 50%;
  transform: translate(-50%, 6px) scale(0.96);
  opacity: 0;
  font-family: var(--font-label);
  font-size: clamp(14px, 1vw, 17px);
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-dark);
  white-space: nowrap;
  padding: 0.35rem 0.7rem;
  border-radius: 2px;
  background: rgba(252, 247, 238, 0.42);
  text-shadow: 0 1px 8px rgba(252, 247, 238, 0.9);
  pointer-events: none;
  transition: opacity 0.4s var(--ease-out), transform 0.4s var(--ease-out);
}

.flower:hover .hotspot-label,
.flower.synced .hotspot-label,
.flower.guided .hotspot-label {
  opacity: 1;
  transform: translate(-50%, 0) scale(1);
}

@media (max-width: 1024px) {
  .plum-layer {
    width: 52%;
  }
}

@media (max-width: 768px) {
  .plum-layer {
    top: 0;
    width: 68%;
  }

  .flower {
    width: 40px;
    height: 40px;
    margin: -20px 0 0 -20px;
  }
}
</style>
