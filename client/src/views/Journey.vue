<template>
  <div class="journey-page">
    <!-- Fixed landscape background -->
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

    <!-- Fixed experience nodes -->
    <div class="node-field">
      <div
        v-for="(n, i) in nodes"
        :key="n.year + n.title"
        class="node"
        :class="{ lit: litIndex === i, dimmed: hoverIndex !== -1 && hoverIndex !== i, pulse: pulseIndex === i }"
        :style="{ left: n.x, top: n.y }"
        @click="toggleNode(i)"
        @mouseenter="hoverIndex = i"
        @mouseleave="hoverIndex = -1"
      >
        <span class="node-halo"></span>
        <span class="node-dot"></span>
        <div class="node-label">
          <p class="node-year">{{ n.year }}</p>
          <transition name="title-fade">
            <p v-if="hoverIndex === i || litIndex === i" class="node-title">{{ n.title }}</p>
          </transition>
        </div>
      </div>
    </div>

    <!-- Hover summary card -->
    <transition name="summary">
      <div
        v-if="hoverIndex !== -1 && openIndex === -1"
        class="summary-card"
        :style="summaryPos"
      >
        <p class="summary-year">{{ nodes[hoverIndex].year }}</p>
        <h4 class="summary-title">{{ nodes[hoverIndex].title }}</h4>
        <p class="summary-desc">{{ nodes[hoverIndex].desc }}</p>
      </div>
    </transition>

    <!-- Click detail card (right side) -->
    <transition name="panel">
      <div v-if="openIndex !== -1" class="detail-panel">
        <p class="panel-year">{{ nodes[openIndex].year }}</p>
        <h3 class="panel-title">{{ nodes[openIndex].title }}</h3>
        <p class="panel-intro">{{ nodes[openIndex].desc }}</p>
        <div class="panel-body">
          <p v-for="d in nodes[openIndex].details" :key="d" class="panel-detail">{{ d }}</p>
        </div>
        <button class="panel-close" @click="openIndex = -1" aria-label="关闭">×</button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import bgSrc from '../assets/pages/journey-bg.png'

const openIndex = ref(-1)
const hoverIndex = ref(-1)
const litIndex = ref(-1)
const pulseIndex = ref(-1)
const showHint = ref(false)
let guideTl = null

const nodes = [
  { year: '2024', title: '校园经历', desc: '校园项目与能力积累', x: '22%', y: '45%', details: ['占位内容：校园项目经历', '占位内容：能力积累'] },
  { year: '2025', title: '海外 SEO / 内容增长', desc: '海外内容增长与数据分析', x: '18%', y: '53%', details: ['占位内容：海外内容增长', '占位内容：数据分析'] },
  { year: '2025', title: '达人商务 / 内容运营', desc: '内容合作与项目执行', x: '29%', y: '59%', details: ['占位内容：内容合作', '占位内容：项目执行'] },
  { year: '2026', title: '产品运营', desc: '产品分析与用户增长', x: '25%', y: '75%', details: ['占位内容：产品分析', '占位内容：用户增长'] },
  { year: '2026', title: 'AI × Product', desc: 'AI 产品探索与应用实践', x: '40%', y: '81%', details: ['占位内容：AI 产品探索', '占位内容：应用实践'] },
  { year: 'NOW', title: 'AI + Coding', desc: '独立项目与技术实践', x: '50%', y: '90%', details: ['占位内容：独立项目', '占位内容：技术实践'] }
]

const summaryPos = computed(() => {
  const n = hoverIndex.value >= 0 ? nodes[hoverIndex.value] : null
  if (!n) return {}
  const x = parseFloat(n.x)
  // card to the right of the node, clamped to avoid overflow
  const left = Math.min(x + 9, 62)
  return { left: left + '%', top: n.y }
})

function toggleNode(i) {
  if (openIndex.value === i) {
    openIndex.value = -1
    return
  }
  openIndex.value = i
  // click pulse on the node
  pulseIndex.value = i
  setTimeout(() => { pulseIndex.value = -1 }, 550)
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
})
</script>

<style scoped>
.journey-page {
  position: relative;
  min-height: 100vh;
  height: 100vh;
  overflow: hidden;
}

.journey-bg {
  position: fixed;
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
  position: fixed;
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
  position: fixed;
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
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

/* Experience nodes — larger, more visible */
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
  opacity: 0.35;
}

.node-halo {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 84px;
  height: 84px;
  margin: -42px 0 0 -42px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(190, 138, 118, 0.5) 0%, rgba(190, 138, 118, 0.16) 50%, transparent 72%);
  opacity: 0.2;
  pointer-events: none;
  animation: breathe 5.5s ease-in-out infinite;
}

.node:nth-child(2) .node-halo { animation-duration: 6.5s; }
.node:nth-child(3) .node-halo { animation-duration: 4.5s; }
.node:nth-child(4) .node-halo { animation-duration: 7s; }
.node:nth-child(5) .node-halo { animation-duration: 5s; }
.node:nth-child(6) .node-halo { animation-duration: 6s; }

@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.2; }
  50% { transform: scale(1.08); opacity: 0.32; }
}

.node-dot {
  position: relative;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #b0766b;
  opacity: 0.8;
  box-shadow: 0 0 10px rgba(176, 118, 107, 0.35);
  transition: opacity 0.4s var(--ease-out), transform 0.4s var(--ease-out);
}

.node:hover .node-dot,
.node.lit .node-dot {
  opacity: 1;
  transform: scale(1.3);
}

.node:hover .node-halo,
.node.lit .node-halo {
  opacity: 0.5;
}

/* Click pulse */
.node.pulse .node-halo {
  animation: haloFlash 0.55s ease-out;
}

@keyframes haloFlash {
  0% { transform: scale(1); opacity: 0.55; }
  100% { transform: scale(1.7); opacity: 0; }
}

.node-label {
  margin-left: var(--space-lg);
  display: flex;
  flex-direction: column;
}

.node-year {
  font-family: var(--font-label);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: 0.16em;
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

/* Hover summary card */
.summary-card {
  position: fixed;
  transform: translateY(-50%);
  z-index: 3;
  width: min(260px, 70vw);
  padding: var(--space-md) var(--space-lg);
  background: linear-gradient(rgba(246, 238, 224, 0.8), rgba(246, 238, 224, 0.8)),
    url('@/assets/textures/paper-texture.svg');
  background-size: auto, 300px;
  box-shadow: 0 2px 18px rgba(58, 51, 46, 0.08);
  pointer-events: none;
}

.summary-year {
  font-family: var(--font-label);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: 0.18em;
  margin: 0 0 0.3rem;
}

.summary-title {
  font-family: var(--font-editorial);
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin: 0 0 0.4rem;
}

.summary-desc {
  font-family: var(--font-body);
  font-size: 0.84rem;
  color: var(--ink-light);
  line-height: 1.6;
  margin: 0;
}

.summary-enter-active,
.summary-leave-active {
  transition: opacity 0.4s var(--ease-out), transform 0.4s var(--ease-out);
}
.summary-enter-from,
.summary-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(-8px);
}

/* Click detail card — right side */
.detail-panel {
  position: fixed;
  right: 20%;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  width: min(600px, 80vw);
  max-height: 78vh;
  overflow-y: auto;
  padding: var(--space-2xl);
  background: linear-gradient(rgba(246, 238, 224, 0.78), rgba(246, 238, 224, 0.78)),
    url('@/assets/textures/paper-texture.svg');
  background-size: auto, 300px;
  box-shadow: 0 2px 28px rgba(58, 51, 46, 0.09);
}

.detail-panel::-webkit-scrollbar {
  width: 4px;
}
.detail-panel::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.22);
  border-radius: 2px;
}

.panel-year {
  font-family: var(--font-label);
  font-size: 0.76rem;
  font-weight: 500;
  color: var(--ink);
  letter-spacing: 0.18em;
  margin: 0 0 0.4rem;
}

.panel-title {
  font-family: var(--font-editorial);
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin: 0 0 0.5rem;
}

.panel-intro {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--ink-light);
  margin: 0 0 var(--space-lg);
}

.panel-body {
  border-top: 1px solid rgba(139, 132, 120, 0.16);
  padding-top: var(--space-md);
}

.panel-detail {
  font-family: var(--font-body);
  font-size: 0.92rem;
  font-weight: 400;
  color: var(--ink);
  line-height: 1.8;
  margin: 0 0 0.5rem;
}

.panel-close {
  position: absolute;
  top: var(--space-md);
  right: var(--space-md);
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--ink-light);
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  transition: color var(--dur-fast) var(--ease-out);
}

.panel-close:hover {
  color: var(--ink-dark);
}

.panel-enter-active,
.panel-leave-active {
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
}
.panel-enter-from,
.panel-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(24px);
}

@media (max-width: 768px) {
  .detail-panel {
    right: 4%;
    width: 80vw;
    padding: var(--space-xl);
  }
  .summary-card {
    width: 60vw;
  }
  .node-label {
    margin-left: var(--space-md);
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
  .node-halo {
    width: 60px;
    height: 60px;
    margin: -30px 0 0 -30px;
  }
}
</style>
