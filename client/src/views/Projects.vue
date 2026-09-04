<template>
  <div class="projects-page" :class="sceneState">
    <!-- Scene coordinate box (matches background cover box exactly) -->
    <div class="scene-box">
      <!-- Unified background frame (dark + lit share one coordinate space) -->
      <div class="bg-frame">
        <!-- Dark background -->
        <img ref="darkRef" class="bg-img bg-dark" :src="darkSrc" :style="darkRegStyle" alt="" aria-hidden="true" />
        <!-- Lit background (registration base) -->
        <img ref="litRef" class="bg-img bg-lit" :src="litSrc" alt="" aria-hidden="true" />
      </div>
      <!-- Fog layer (disperses after lighting) -->
      <img ref="fogRef" class="bg-img bg-fog" :src="fogSrc" alt="" aria-hidden="true" />

      <!-- Lamp core flash (small, bound to lamp shade) -->
      <div ref="coreRef" class="lamp-core" :class="{ hovered: lampHover }" :style="lampStyle" aria-hidden="true"></div>
      <!-- Lamp breathing glow (dark-state idle hint, separate from flash) -->
      <div class="lamp-glow" :class="{ hovered: lampHover }" :style="lampStyle" aria-hidden="true"></div>

      <!-- Guide text (shares lamp anchor) -->
      <p
        ref="guideRef"
        class="guide-text"
        :class="{ hovered: lampHover }"
        :style="guideStyle"
        @click="toggleScene"
      >点灯 · 查看我的项目</p>

      <!-- Lamp hotspot (transparent, shares lamp anchor) -->
      <div
        class="lamp-hotspot"
        :style="hotspotStyle"
        @click="toggleScene"
        @mouseenter="lampHover = true"
        @mouseleave="lampHover = false"
      ></div>
    </div>

    <!-- Central content -->
    <div ref="contentLayerRef" class="content-layer">
      <h1 ref="titleRef" class="content-title">我的项目</h1>
      <p ref="subRef" class="content-sub">从问题出发，把想法真正做出来。</p>
      <div class="project-list">
        <div
          v-for="(p, i) in projects"
          :key="p.num"
          class="project-item"
          :ref="el => setProjRef(el, i)"
        >
          <span class="project-num">{{ p.num }}</span>
          <div class="project-body">
            <h3 class="project-title">{{ p.title }}</h3>
            <p class="project-tags">{{ p.tags }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import darkSrc from '../assets/pages/projects/projects-dark.png'
import litSrc from '../assets/pages/projects/projects-lit.png'
import fogSrc from '../assets/pages/projects/projects-fog.png'

const sceneState = ref('dark') // 'dark' | 'transitioning' | 'lit'
const lampHover = ref(false)

const darkRef = ref(null)
const litRef = ref(null)
const fogRef = ref(null)
const coreRef = ref(null)
const guideRef = ref(null)
const titleRef = ref(null)
const subRef = ref(null)
const contentLayerRef = ref(null)
const projRefs = [ref(null), ref(null), ref(null)]

let projectsTimeline = null

// Lamp anchor in design coordinates (1912x948 design canvas), centralized for easy tuning
const PROJECTS_SCENE = {
  baseWidth: 1912,
  baseHeight: 948,
  lamp: {
    x: 190,
    y: 620,
    hotspotWidth: 90,
    hotspotHeight: 130,
    guideOffsetX: 100,
    guideOffsetY: 5
  }
}

// Convert design px to percentages (shared by lamp, hotspot, guide)
const L = PROJECTS_SCENE.lamp
const pct = (v, base) => (v / base) * 100
const lampX = pct(L.x, PROJECTS_SCENE.baseWidth)         // 9.94%
const lampY = pct(L.y, PROJECTS_SCENE.baseHeight)        // 65.40%
const hotW = pct(L.hotspotWidth, PROJECTS_SCENE.baseWidth)   // 4.71%
const hotH = pct(L.hotspotHeight, PROJECTS_SCENE.baseHeight) // 13.71%
const guideOffX = pct(L.guideOffsetX, PROJECTS_SCENE.baseWidth)  // 5.23%
const guideOffY = pct(L.guideOffsetY, PROJECTS_SCENE.baseHeight) // 0.53%

// Shared anchor styles — lamp core / hotspot / guide all derive from PROJECTS_SCENE.lamp
const lampStyle = { left: lampX + '%', top: lampY + '%' }
const hotspotStyle = { left: lampX + '%', top: lampY + '%', width: hotW + '%', height: hotH + '%' }
const guideStyle = { left: (lampX + guideOffX) + '%', top: (lampY + guideOffY) + '%' }

// Dark/lit image registration — dark aligns to lit (base). Actual image size 1672x941.
const IMG_W = 1672
const IMG_H = 941
const PROJECTS_IMAGE_REGISTRATION = {
  dark: { scale: 1, x: 0, y: 0 } // px correction in image coordinates
}
const regD = PROJECTS_IMAGE_REGISTRATION.dark
const darkRegStyle = {
  transform: `translate(${(regD.x / IMG_W) * 100}%, ${(regD.y / IMG_H) * 100}%) scale(${regD.scale})`
}

// Single-layer fog dispersion (design px, converted to scene % for scale-invariant drift)
const FOG_DISPERSION = { x: 45, y: -12, scale: 1.04, duration: 2.0 }

const projects = [
  { num: '01', title: 'AI 情报系统', tags: 'AI / 数据 / 自动化' },
  { num: '02', title: 'KOL 建联 Agent', tags: 'AI / Agent / 增长' },
  { num: '03', title: '个人知识库', tags: 'AI / 产品 / 知识管理' }
]

function setProjRef(el, i) {
  if (el) projRefs[i].value = el
}

function toggleScene() {
  if (sceneState.value === 'transitioning') return
  if (sceneState.value === 'dark') {
    sceneState.value = 'transitioning'
    projectsTimeline.play()
  } else if (sceneState.value === 'lit') {
    sceneState.value = 'transitioning'
    projectsTimeline.reverse()
  }
}

onMounted(() => {
  // Debug registration mode — add ?debug-register to URL to see both at 0.5 opacity
  const debugRegister = new URLSearchParams(window.location.search).has('debug-register')
  if (debugRegister) {
    gsap.set(darkRef.value, { opacity: 0.5 })
    gsap.set(litRef.value, { opacity: 0.5 })
    if (fogRef.value) gsap.set(fogRef.value, { opacity: 0 })
    return
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) {
    sceneState.value = 'lit'
    gsap.set([darkRef.value], { opacity: 0 })
    gsap.set([litRef.value], { opacity: 1 })
    gsap.set([fogRef.value], { opacity: 0 })
    gsap.set([titleRef.value, subRef.value, ...projRefs.map(r => r.value)], { opacity: 1, y: 0 })
    return
  }

  projectsTimeline = gsap.timeline({
    paused: true,
    onComplete: () => { sceneState.value = 'lit' },
    onReverseComplete: () => { sceneState.value = 'dark' },
    onReverseStart: () => {
      // Immediately disable project interaction when reversing
      if (contentLayerRef.value) {
        contentLayerRef.value.style.pointerEvents = 'none'
      }
    }
  })
    // 0.00s lamp core flash
    .to(coreRef.value, { opacity: 0.55, scale: 1, duration: 0.3, ease: 'power2.out' }, 0)
    .to(coreRef.value, { opacity: 0, duration: 0.6, ease: 'power2.inOut' }, 0.5)
    // 0.10s guide text fades
    .to(guideRef.value, { opacity: 0, y: -6, duration: 0.35, ease: 'power2.in' }, 0.1)
    // 0.20s lit fades in, 0.25s dark fades out (crossfade)
    .to(litRef.value, { opacity: 1, duration: 1.8, ease: 'power2.inOut' }, 0.2)
    .to(darkRef.value, { opacity: 0, duration: 1.8, ease: 'power2.inOut' }, 0.25)
    // 0.35s fog disperses (up-right, single layer)
    .to(fogRef.value, {
      opacity: 0,
      xPercent: (FOG_DISPERSION.x / IMG_W) * 100,
      yPercent: (FOG_DISPERSION.y / IMG_H) * 100,
      scale: FOG_DISPERSION.scale,
      duration: FOG_DISPERSION.duration,
      ease: 'sine.out'
    }, 0.35)
    // 1.15s enable content layer (visibility + pointer-events), title appears
    .set(contentLayerRef.value, { visibility: 'visible', pointerEvents: 'auto' }, 1.15)
    .to(titleRef.value, { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 1.15)
    // 1.30s subtitle
    .to(subRef.value, { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 1.3)
    // 1.45s project 01
    .to(projRefs[0].value, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 1.45)
    // 1.60s project 02
    .to(projRefs[1].value, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 1.6)
    // 1.75s project 03
    .to(projRefs[2].value, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 1.75)

  // first-visit entry cue: guide text gently appears once, then rests
  gsap.fromTo(
    guideRef.value,
    { opacity: 0, y: 6 },
    { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out', delay: 0.7 }
  )
})

onUnmounted(() => {
  if (projectsTimeline) projectsTimeline.kill()
})
</script>

<style scoped>
.projects-page {
  position: relative;
  height: 100dvh;
  min-height: 100vh;
  overflow: hidden;
}

/* Scene coordinate box — matches cover-rendered background exactly */
.scene-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: max(100%, calc(100dvh * 1.7768));
  aspect-ratio: 1672 / 941;
  pointer-events: none;
  z-index: 0;
}

/* Unified background frame — dark + lit share one scale/translate/cover mapping */
.bg-frame {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* Background images — fully stacked, shared coordinate space */
.bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.bg-dark { opacity: 1; }
.bg-lit { opacity: 0; }
.bg-fog { opacity: 1; }

/* Lamp core flash — bound to real lamp shade (position via lampStyle) */
.lamp-core {
  position: absolute;
  transform: translate(-50%, -50%) scale(0.8);
  width: 3%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 232, 190, 0.9) 0%, rgba(255, 210, 150, 0.4) 55%, transparent 100%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s var(--ease-out);
}

.lamp-core.hovered {
  opacity: 0.3;
}

/* Lamp breathing glow — dark-state idle hint, separate from GSAP flash */
.lamp-glow {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 4%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 218, 160, 0.5) 0%, rgba(255, 198, 130, 0.22) 55%, transparent 100%);
  opacity: 0;
  pointer-events: none;
  animation: lamp-breathe 4.5s ease-in-out infinite;
}

@keyframes lamp-breathe {
  0%, 100% { opacity: 0.14; }
  50% { opacity: 0.28; }
}

.lamp-glow.hovered {
  animation: none;
  opacity: 0.42;
}

/* Guide text (position via guideStyle, derived from lamp anchor) */
.guide-text {
  position: absolute;
  margin: 0;
  font-family: var(--font-label);
  font-size: 0.85rem;
  letter-spacing: 0.14em;
  color: rgba(245, 240, 230, 0.92);
  cursor: pointer;
  padding: 0.6rem 0.9rem;
  text-shadow: 0 1px 8px rgba(15, 18, 18, 0.55);
  pointer-events: auto;
  z-index: 3;
  opacity: 0;
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out),
              transform var(--dur-fast) var(--ease-out);
}

.guide-text:hover,
.guide-text.hovered {
  color: rgba(255, 250, 242, 1);
  letter-spacing: 0.18em;
  transform: translateX(3px);
}

/* Lamp hotspot — transparent rectangle, bound to real lamp (size via hotspotStyle) */
.lamp-hotspot {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  pointer-events: auto;
  z-index: 4;
  background: transparent;
}

/* Content layer — centered, fully disabled until lit */
.content-layer {
  position: absolute;
  left: 50%;
  top: 52%;
  transform: translate(-50%, -50%);
  z-index: 1;
  width: min(520px, 86vw);
  text-align: center;
  visibility: hidden;
  pointer-events: none;
}

.content-title {
  font-family: var(--font-editorial);
  font-size: clamp(1.8rem, 3.4vw, 2.6rem);
  font-weight: 400;
  color: var(--ink-dark);
  letter-spacing: 0.06em;
  margin: 0 0 var(--space-sm);
  opacity: 0;
  transform: translateY(16px);
  text-shadow: 0 1px 14px rgba(252, 247, 238, 0.7);
}

.content-sub {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--ink);
  letter-spacing: 0.04em;
  margin: 0 0 var(--space-xl);
  opacity: 0;
  transform: translateY(16px);
  text-shadow: 0 1px 12px rgba(252, 247, 238, 0.7);
}

.project-list {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.project-item {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
  padding: var(--space-md) 0;
  border-top: 1px solid rgba(139, 132, 120, 0.2);
  cursor: pointer;
  opacity: 0;
  transform: translateY(16px);
}

.project-item:hover {
  opacity: 0.72;
}

.project-num {
  font-family: var(--font-label);
  font-size: 0.68rem;
  color: var(--bark);
  letter-spacing: 0.1em;
  flex-shrink: 0;
}

.project-title {
  font-family: var(--font-editorial);
  font-size: 1.12rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.03em;
  margin: 0;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
}

.project-tags {
  font-family: var(--font-label);
  font-size: 0.64rem;
  font-weight: 500;
  color: var(--ink-green);
  letter-spacing: 0.08em;
  margin: 0.15rem 0 0;
}

@media (max-width: 768px) {
  .guide-text {
    font-size: 0.6rem;
  }
  .content-layer {
    width: 88vw;
    top: 50%;
  }

  .project-item {
    padding: var(--space-sm) 0;
  }

  .project-tags {
    line-height: 1.45;
  }
}
</style>
