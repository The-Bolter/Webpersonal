<template>
  <div class="plum-layer">
    <div ref="recoilRef" class="plum-recoil">
      <div ref="wrapperRef" class="plum-wrapper">
        <div ref="innerRef" class="plum-inner">
          <img :src="plumSrc" alt="" class="plum-image" />

          <div
            v-for="f in flowers"
            :key="f.id"
            class="flower"
            :class="[f.id, { synced: store.hoveredId === f.id }]"
            :style="{ left: f.x + '%', top: f.y + '%' }"
            @mouseenter="onFlowerEnter(f)"
            @mouseleave="store.clearHovered"
            @click="onFlowerClick(f, $event)"
          >
            <span class="flower-halo"></span>
            <span class="hotspot-label">{{ f.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import plumSrc from '../assets/index/plum/plum-branch.png'
import { useAppStore } from '../store'

const store = useAppStore()
const router = useRouter()
const recoilRef = ref(null)
const wrapperRef = ref(null)
const innerRef = ref(null)
let windTl = null
let driftTl = null

const flowers = [
  { id: 'projects', label: 'PROJECTS', x: 48.7, y: 29.9, rx: 30, ry: 82, to: '/projects' },
  { id: 'journey', label: 'JOURNEY', x: 29.0, y: 63.0, rx: 42, ry: 86, to: '/journey' },
  { id: 'studio', label: 'STUDIO', x: 20.4, y: 54.8, rx: 54, ry: 83, to: '/studio' },
  { id: 'about', label: 'ABOUT', x: 52.8, y: 67.0, rx: 66, ry: 87, to: '/about' },
  { id: 'contact', label: 'CONTACT', x: 78.0, y: 25.9, rx: 78, ry: 81, to: '/contact' }
]

function onFlowerEnter(f) {
  store.setHovered(f.id)
  store.triggerRipple(f.id, f.rx, f.ry, 0.6)
}

function onFlowerClick(f, event) {
  const el = event.currentTarget
  // Flower pulse
  gsap.timeline()
    .to(el, { scale: 1.08, rotation: 3, duration: 0.25, ease: 'power2.out' })
    .to(el, { scale: 1, rotation: 0, duration: 0.9, ease: 'sine.inOut' })
  // Whole-branch recoil (separate layer, no conflict with wind)
  if (recoilRef.value) {
    gsap.timeline()
      .to(recoilRef.value, { x: 3, y: 1, rotation: 0.4, duration: 0.3, ease: 'power2.out' })
      .to(recoilRef.value, { x: 0, y: 0, rotation: 0, duration: 1.4, ease: 'sine.inOut' })
  }
  // Stronger ripple
  store.triggerRipple(f.id, f.rx, f.ry, 1.6)
  // Navigate after brief feedback
  setTimeout(() => router.push(f.to), 350)
}

onMounted(() => {
  const el = wrapperRef.value
  const inner = innerRef.value
  if (!el || !inner) return

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return

  // Wind — outer sway (pivot at root, top-right)
  windTl = gsap.timeline({
    delay: 5.5,
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
    delay: 5.8,
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
})
</script>

<style scoped>
.plum-layer {
  position: fixed;
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

.flower-halo {
  position: absolute;
  inset: -20px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 222, 196, 0.55) 0%, rgba(255, 222, 196, 0.16) 48%, transparent 72%);
  opacity: 0.16;
  transition: opacity 0.5s var(--ease-out);
  pointer-events: none;
}

/* Idle life — different rhythm per flower */
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

/* Hover / synced state */
.flower:hover .flower-halo,
.flower.synced .flower-halo {
  opacity: 0.5;
}

.hotspot-label {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translate(-50%, 4px);
  opacity: 0;
  font-family: var(--font-label);
  font-size: 0.56rem;
  font-weight: 400;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--ink-green);
  white-space: nowrap;
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
  pointer-events: none;
}

.flower:hover .hotspot-label,
.flower.synced .hotspot-label {
  opacity: 1;
  transform: translate(-50%, 0);
}
</style>
