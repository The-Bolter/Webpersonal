<template>
  <div class="journey-page">
    <!-- Scene coordinate box: background and nodes use one cover mapping -->
    <div class="journey-scene">
      <div class="journey-bg" aria-hidden="true">
        <img :src="bgSrc" alt="" />
      </div>

      <!-- Subtle stream motion overlay -->
      <div class="stream-motion" aria-hidden="true">
        <div class="stream-band band-1"></div>
        <div class="stream-band band-2"></div>
      </div>

      <!-- First-visit hint -->
      <transition name="hint-fade">
        <p v-if="showHint" class="journey-hint">沿溪而行，探索我的经历</p>
      </transition>

      <!-- Experience nodes (Scene Layer) -->
      <div class="node-field">
        <div
          v-for="(n, i) in nodes"
          :key="n.id"
          class="node"
          :class="{
            now: n.id === 'now',
            lit: litIndex === i,
            dimmed: hoverIndex !== -1 && hoverIndex !== i,
            active: openIndex === i
          }"
          :style="{ left: n.x, top: n.y }"
          @click="toggleNode(i)"
          @mouseenter="hoverIndex = i"
          @mouseleave="hoverIndex = -1"
        >
          <span class="node-point">
            <span class="node-halo"></span>
            <span class="node-dot"></span>
          </span>
          <div class="node-label">
            <p class="node-year">{{ n.year }}</p>
            <transition name="title-fade">
              <p v-if="hoverIndex === i || litIndex === i || openIndex === i" class="node-title">{{ n.title }}</p>
            </transition>
          </div>
          <span class="node-tick" aria-hidden="true"></span>
        </div>
      </div>
    </div>

    <!-- Reading pane (UI Layer) — fixed right-side 题记区 -->
    <transition name="pane">
      <div v-if="openIndex !== -1" ref="paneRef" class="journey-reading-pane">
        <div class="pane-veil" aria-hidden="true"></div>
        <div class="pane-content">
          <p class="pane-year">{{ nodes[openIndex].year }}</p>
          <h3 class="pane-title">{{ nodes[openIndex].title }}</h3>
          <p class="pane-intro">{{ nodes[openIndex].desc }}</p>
          <div class="pane-rule" aria-hidden="true"></div>
          <div class="pane-sections">
            <div v-for="s in activeSections" :key="s.num" class="pane-section">
              <p class="pane-section-head">
                <span class="pane-section-num">{{ s.num }}</span>
                <span class="pane-section-label">{{ s.label }}</span>
              </p>
              <p class="pane-section-text">{{ s.text }}</p>
            </div>
          </div>
          <button class="pane-collapse" @click="closeDetail">收起</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import bgSrc from '../assets/pages/journey-bg-v2.png'

const openIndex = ref(-1)
const hoverIndex = ref(-1)
const litIndex = ref(-1)
const showHint = ref(false)
let guideTl = null
let detailTl = null

const paneRef = ref(null)

// Journey nodes — centralized config for manual tuning (design % within scene coordinate space)
// Coordinates are manually calibrated — DO NOT modify x/y.
const JOURNEY_NODES = [
  { id: 'campus', year: '2024', title: '校园经历', desc: '校园项目与能力积累', x: '20%', y: '45%', details: ['占位内容：校园项目经历', '占位内容：能力积累'] },
  { id: 'seo', year: '2025', title: '海外 SEO / 内容增长', desc: '海外内容增长与数据分析', x: '18%', y: '54%', details: ['占位内容：海外内容增长', '占位内容：数据分析'] },
  { id: 'kol', year: '2025', title: '达人商务 / 内容运营', desc: '内容合作与项目执行', x: '32%', y: '59%', details: ['占位内容：内容合作', '占位内容：项目执行'] },
  { id: 'product', year: '2026', title: '产品运营', desc: '产品分析与用户增长', x: '22%', y: '72%', details: ['占位内容：产品分析', '占位内容：用户增长'] },
  { id: 'aixp', year: '2026', title: 'AI × Product', desc: 'AI 产品探索与应用实践', x: '40%', y: '77%', details: ['占位内容：AI 产品探索', '占位内容：应用实践'] },
  { id: 'now', year: 'NOW', title: 'AI + Coding', desc: '独立项目与技术实践', x: '55%', y: '87%', details: ['占位内容：独立项目', '占位内容：技术实践'] }
]

const nodes = JOURNEY_NODES

const PANE_SECTIONS = [
  { num: '01', label: '核心工作' },
  { num: '02', label: '项目结果' },
  { num: '03', label: '能力沉淀' }
]

const activeSections = computed(() => {
  if (openIndex.value === -1) return []
  const details = nodes[openIndex.value].details || []
  const texts = details.concat(['占位内容：待补充', '占位内容：待补充']).slice(0, 3)
  return PANE_SECTIONS.map((s, i) => ({ ...s, text: texts[i] }))
})

function animateContentOut(done) {
  const content = paneRef.value ? paneRef.value.querySelector('.pane-content') : null
  if (!content) {
    done && done()
    return
  }
  if (detailTl) detailTl.kill()
  detailTl = gsap.timeline({ onComplete: done })
  detailTl.to(content, { opacity: 0, y: -5, duration: 0.25, ease: 'power2.in' })
}

function animateContentIn() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const pane = paneRef.value
  if (!pane) return
  const content = pane.querySelector('.pane-content')
  const year = pane.querySelector('.pane-year')
  const title = pane.querySelector('.pane-title')
  const rule = pane.querySelector('.pane-rule')
  const intro = pane.querySelector('.pane-intro')
  const sections = pane.querySelectorAll('.pane-section')

  if (detailTl) detailTl.kill()

  if (reduceMotion) {
    gsap.set([content, year, title, intro, ...sections], { opacity: 1, y: 0 })
    gsap.set(rule, { scaleX: 1 })
    return
  }

  gsap.set(content, { opacity: 1, y: 0 })
  gsap.set([year, title, intro], { opacity: 0, y: 5 })
  gsap.set(rule, { scaleX: 0, transformOrigin: 'left center' })
  gsap.set(sections, { opacity: 0, y: 8 })

  detailTl = gsap.timeline()
    .to(year, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.10)
    .to(title, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.20)
    .to(rule, { scaleX: 1, duration: 0.35, ease: 'sine.out' }, 0.30)
    .to(intro, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.40)
    .to(sections, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out', stagger: 0.12 }, 0.50)
}

function openNode(i) {
  openIndex.value = i
  nextTick(animateContentIn)
}

function toggleNode(i) {
  if (openIndex.value === i) {
    closeDetail()
    return
  }
  if (openIndex.value !== -1) {
    animateContentOut(() => openNode(i))
  } else {
    openNode(i)
  }
}

function closeDetail() {
  if (openIndex.value === -1) return
  if (detailTl) detailTl.kill()
  openIndex.value = -1
}

onMounted(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return

  if (!sessionStorage.getItem('journey_hint_seen')) {
    setTimeout(() => {
      showHint.value = true
      sessionStorage.setItem('journey_hint_seen', '1')

      guideTl = gsap.timeline({ onComplete: () => { litIndex.value = -1 } })
      nodes.forEach((_, i) => {
        guideTl.add(() => { litIndex.value = i })
        guideTl.to({}, { duration: 0.5 })
      })
      guideTl.add(() => { litIndex.value = -1 })

      setTimeout(() => { showHint.value = false }, 3200)
    }, 900)
  }
})

onUnmounted(() => {
  if (guideTl) guideTl.kill()
  if (detailTl) detailTl.kill()
})
</script>

<style scoped>
.journey-page {
  position: relative;
  height: 100dvh;
  min-height: 100vh;
  overflow: hidden;
}

.journey-scene {
  position: absolute;
  top: 50%;
  left: 50%;
  width: max(100%, calc(100dvh * 1.7768));
  aspect-ratio: 16 / 9;
  transform: translate(-50%, -50%);
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.journey-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.journey-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Stream motion */
.stream-motion {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.stream-band {
  position: absolute;
  left: 42%;
  width: 18%;
  height: 160%;
  top: -30%;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(255, 248, 236, 0.06) 30%,
    transparent 55%,
    rgba(255, 248, 236, 0.05) 80%,
    transparent 100%
  );
  animation: streamFlow 26s linear infinite;
}

.band-2 {
  opacity: 0.6;
  animation-duration: 38s;
  animation-direction: reverse;
}

@keyframes streamFlow {
  from { transform: translateY(-12%); }
  to { transform: translateY(12%); }
}

/* Hint */
.journey-hint {
  position: absolute;
  top: calc(var(--nav-height) + var(--space-lg));
  left: 50%;
  transform: translateX(-50%);
  z-index: 4;
  margin: 0;
  font-family: var(--font-label);
  font-size: 0.64rem;
  letter-spacing: 0.28em;
  color: var(--ink-green);
  pointer-events: none;
}

.hint-fade-enter-active,
.hint-fade-leave-active {
  transition: opacity 1s var(--ease-out);
}
.hint-fade-enter-from,
.hint-fade-leave-to {
  opacity: 0;
}

/* Node field */
.node-field {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

/* Experience nodes */
.node {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  display: flex;
  align-items: center;
  pointer-events: auto;
  transition: opacity 0.45s var(--ease-out);
}

.node.dimmed {
  opacity: 0.78;
}

.node-point {
  position: relative;
  width: 10px;
  height: 10px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Subtle halo — no hard boundary */
.node-halo {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 26px;
  height: 26px;
  margin: -13px 0 0 -13px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(156, 90, 79, 0.32) 0%, rgba(156, 90, 79, 0.10) 55%, transparent 100%);
  opacity: 0.16;
  pointer-events: none;
  transition: opacity 0.5s var(--ease-out);
}

/* Normal node dot — 10px low-saturation dark cinnabar */
.node-dot {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #9c5a4f;
  transition: transform 0.45s var(--ease-out), opacity 0.45s var(--ease-out);
}

.node:hover .node-dot {
  transform: scale(1.18);
}

.node:hover .node-halo {
  animation: halo-press 0.6s var(--ease-out);
}

@keyframes halo-press {
  0% { transform: scale(1); opacity: 0.16; }
  55% { transform: scale(1.25); opacity: 0.32; }
  100% { transform: scale(1); opacity: 0.16; }
}

/* Active node */
.node.active .node-dot {
  transform: scale(1.2);
}

.node.active .node-halo {
  transform: scale(1.23);
  opacity: 0.42;
}

.node.active .node-year {
  font-weight: 600;
}

.node.lit .node-dot {
  transform: scale(1.15);
}

/* Short ink tick — active node (and NOW always) */
.node-tick {
  margin-left: 12px;
  align-self: center;
  width: 40px;
  height: 1px;
  background: rgba(90, 80, 70, 0.5);
  transform: scaleX(0);
  transform-origin: left center;
  opacity: 0;
  transition: transform 0.5s var(--ease-out), opacity 0.5s var(--ease-out);
  flex-shrink: 0;
}

.node.active .node-tick,
.node.now .node-tick {
  transform: scaleX(1);
  opacity: 1;
}

/* ---- NOW node — the journey's endpoint ---- */
.node.now .node-point {
  width: 14px;
  height: 14px;
}

.node.now .node-dot {
  width: 13px;
  height: 13px;
  background: #7f453c;
}

.node.now .node-halo {
  width: 36px;
  height: 36px;
  margin: -18px 0 0 -18px;
  background: radial-gradient(circle, rgba(140, 76, 64, 0.4) 0%, rgba(140, 76, 64, 0.14) 55%, transparent 100%);
  opacity: 0.28;
  animation: now-pulse 4s ease-in-out infinite;
}

@keyframes now-pulse {
  0%, 100% { transform: scale(1); opacity: 0.28; }
  50% { transform: scale(1.14); opacity: 0.46; }
}

.node.now .node-year {
  color: var(--ink-dark);
  font-weight: 600;
  letter-spacing: 0.26em;
}

.node-label {
  margin-left: var(--space-md);
  display: flex;
  flex-direction: column;
}

.node-year {
  font-family: var(--font-label);
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.22em;
  margin: 0;
}

.node-title {
  font-family: var(--font-editorial);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin: 0.15rem 0 0;
  white-space: nowrap;
}

.title-fade-enter-active,
.title-fade-leave-active {
  transition: opacity 0.45s var(--ease-out), transform 0.45s var(--ease-out);
}
.title-fade-enter-from,
.title-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* ---- Reading pane (UI Layer) — mid-right 题记区 ---- */
.journey-reading-pane {
  position: absolute;
  left: 45%;
  top: 14%;
  width: clamp(360px, 38vw, 640px);
  max-width: 640px;
  height: auto;
  z-index: 6;
  pointer-events: auto;
}

.journey-reading-pane::-webkit-scrollbar {
  width: 4px;
}
.journey-reading-pane::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.22);
  border-radius: 2px;
}

/* Borderless fog veil — readability only, no card outline */
.pane-veil {
  position: absolute;
  inset: -10% -6%;
  background: radial-gradient(ellipse at center, rgba(252, 247, 238, 0.5) 0%, rgba(252, 247, 238, 0.22) 55%, transparent 82%);
  z-index: -1;
  pointer-events: none;
}

.pane-content {
  position: relative;
  padding: var(--space-xl) var(--space-lg);
}

.pane-year {
  font-family: var(--font-label);
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--bark);
  letter-spacing: 0.18em;
  margin: 0 0 0.4rem;
}

.pane-title {
  font-family: var(--font-editorial);
  font-size: clamp(1.4rem, 2vw, 1.7rem);
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.pane-intro {
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--ink-light);
  margin: 0 0 var(--space-md);
}

/* Thin ink divider between intro and sections */
.pane-rule {
  width: 100%;
  height: 1px;
  background: rgba(139, 132, 120, 0.28);
  margin: 0 0 var(--space-lg);
  transform: scaleX(0);
}

.pane-sections {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.pane-section-head {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  margin: 0 0 0.2rem;
}

.pane-section-num {
  font-family: var(--font-label);
  font-size: 0.66rem;
  font-weight: 500;
  color: var(--bark);
  letter-spacing: 0.1em;
}

.pane-section-label {
  font-family: var(--font-editorial);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.05em;
}

.pane-section-text {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--ink);
  line-height: 1.75;
  margin: 0;
  padding-left: 1.9rem;
}

.pane-collapse {
  display: inline-block;
  margin-top: var(--space-lg);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-label);
  font-size: 0.66rem;
  letter-spacing: 0.16em;
  color: var(--ink-light);
  padding: 0.3rem 0;
  transition: color var(--dur-fast) var(--ease-out);
}

.pane-collapse:hover {
  color: var(--ink-dark);
}

/* Pane fade transition */
.pane-enter-active,
.pane-leave-active {
  transition: opacity 0.5s var(--ease-out);
}
.pane-enter-from,
.pane-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .journey-scene {
    width: max(100%, calc(100dvh * 1.35));
    aspect-ratio: 1.35;
  }

  .node-label {
    margin-left: var(--space-sm);
  }
  .node-year {
    font-size: 0.7rem;
  }
  .node-title {
    font-size: 0.82rem;
    white-space: normal;
    max-width: 120px;
    line-height: 1.4;
  }

  .journey-reading-pane {
    left: 50%;
    top: 30%;
    transform: translateX(-50%);
    width: min(76vw, 420px);
    height: auto;
  }
}
</style>
