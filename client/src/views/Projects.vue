<template>
  <div class="projects-page">
    <!-- Fixed landscape background -->
    <div class="project-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" />
    </div>

    <!-- Dark overlay (initial dim) -->
    <div ref="overlayRef" class="dark-overlay" aria-hidden="true"></div>

    <!-- Pavilion glow -->
    <div ref="pavilionRef" class="pavilion-glow" aria-hidden="true"></div>

    <!-- Lamp glow (breathing) -->
    <div ref="lampGlowRef" class="lamp-glow" aria-hidden="true"></div>

    <!-- Guide text (clickable invitation) -->
    <p
      v-if="!isLit"
      ref="guideRef"
      class="guide-text"
      @click="lightUp"
    >点亮灯火，走进我的作品。</p>

    <!-- Lamp hot zone -->
    <div
      v-if="!isLit"
      class="lamp-zone"
      @click="lightUp"
      @mouseenter="lampHover = true"
      @mouseleave="lampHover = false"
    ></div>

    <!-- Central content (hidden until lighting) -->
    <div ref="contentRef" class="content-wrapper">
      <div class="content-sheet">
        <p class="content-eyebrow">PROJECTS</p>
        <h1 class="content-title">精选项目</h1>
        <p class="content-intro">这里记录我真正参与、设计和做出来的事情。</p>

        <div class="project-list">
          <article
            v-for="p in projects"
            :key="p.title"
            class="project-item"
            @click="openProject = p"
          >
            <div class="project-head">
              <span class="project-num">{{ p.num }}</span>
              <div>
                <h3 class="project-title">{{ p.title }}</h3>
                <p class="project-tags">{{ p.tags }}</p>
              </div>
            </div>
            <p class="project-desc">{{ p.desc }}</p>
          </article>
        </div>
      </div>
    </div>

    <!-- Project detail panel -->
    <transition name="detail">
      <div v-if="openProject" class="detail-panel">
        <button class="detail-close" @click="openProject = null" aria-label="关闭">×</button>
        <p class="detail-eyebrow">{{ openProject.num }}</p>
        <h2 class="detail-title">{{ openProject.title }}</h2>
        <p class="detail-tags">{{ openProject.tags }}</p>
        <dl class="detail-fields">
          <div v-for="f in detailFields" :key="f.key" class="detail-field">
            <dt class="detail-label">{{ f.label }}</dt>
            <dd class="detail-value">{{ openProject[f.key] || '占位内容，待补充' }}</dd>
          </div>
        </dl>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import bgSrc from '../assets/pages/project.png'

const isLit = ref(false)
const lampHover = ref(false)
const openProject = ref(null)
const overlayRef = ref(null)
const lampGlowRef = ref(null)
const pavilionRef = ref(null)
const guideRef = ref(null)
const contentRef = ref(null)
let lightTl = null

const projects = [
  {
    num: '01',
    title: 'AI 热点情报系统',
    tags: 'AI × 数据 × 自动化',
    desc: '从信息采集、筛选、评分到 AI 分析，构建一套自动化热点情报系统。',
    background: '', duty: '', problem: '', solution: '', result: '', tech: ''
  },
  {
    num: '02',
    title: 'AI 建联自动分发系统',
    tags: 'AI Agent × 工作流',
    desc: '探索如何让 AI 从信息筛选走向任务执行，完成达人筛选、建联与信息分发。',
    background: '', duty: '', problem: '', solution: '', result: '', tech: ''
  },
  {
    num: '03',
    title: '个人作品集网站',
    tags: 'Vue × GSAP × AI Coding',
    desc: '从视觉设计到交互实现，用 AI Coding 将东方山水视觉概念转化为真实网页。',
    background: '', duty: '', problem: '', solution: '', result: '', tech: ''
  },
  {
    num: '04',
    title: '更多项目',
    tags: '持续探索中',
    desc: '后续再填入真实内容。',
    background: '', duty: '', problem: '', solution: '', result: '', tech: ''
  }
]

const detailFields = [
  { key: 'background', label: '项目背景' },
  { key: 'duty', label: '我的职责' },
  { key: 'problem', label: '核心问题' },
  { key: 'solution', label: '解决方案' },
  { key: 'result', label: '最终结果' },
  { key: 'tech', label: '技术 / 工具' }
]

function lightUp() {
  if (isLit.value) return
  isLit.value = true
  lightTl.play()
}

onMounted(() => {
  // Center the content wrapper using GSAP percent transforms (avoids CSS transform conflict)
  if (contentRef.value) {
    gsap.set(contentRef.value, { xPercent: -50, yPercent: -50, y: 16 })
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) {
    isLit.value = true
    if (contentRef.value) contentRef.value.style.opacity = '1'
    return
  }

  lightTl = gsap.timeline({ paused: true })
    // Stage 1: guide fades + lamp brightens
    .to(guideRef.value, { opacity: 0, y: -6, duration: 0.35, ease: 'power2.in' }, 0)
    .to(lampGlowRef.value, { opacity: 1, scale: 1.6, duration: 0.55, ease: 'power2.out' }, 0)
    // Stage 2: pavilion reveals
    .to(pavilionRef.value, { opacity: 0.65, duration: 0.7, ease: 'power2.inOut' }, 0.5)
    // Stage 3: dark overlay fades
    .to(overlayRef.value, { opacity: 0.08, duration: 0.8, ease: 'power2.inOut' }, 0.4)
    // Stage 4: content appears
    .to(contentRef.value, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.9, ease: 'power2.out' }, 1.0)
})

onUnmounted(() => {
  if (lightTl) lightTl.kill()
})
</script>

<style scoped>
.projects-page {
  position: relative;
  min-height: 100vh;
  height: 100vh;
  overflow: hidden;
}

.project-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.project-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Dark overlay */
.dark-overlay {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: rgba(10, 14, 14, 0.3);
}

/* Pavilion glow */
.pavilion-glow {
  position: fixed;
  left: 85%;
  top: 49%;
  width: 140px;
  height: 140px;
  margin: -70px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 210, 150, 0.6) 0%, rgba(255, 190, 120, 0.2) 50%, transparent 72%);
  opacity: 0;
  z-index: 1;
  pointer-events: none;
}

/* Lamp glow */
.lamp-glow {
  position: fixed;
  left: 17%;
  top: 80%;
  width: 110px;
  height: 110px;
  margin: -55px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 214, 160, 0.85) 0%, rgba(255, 190, 120, 0.3) 45%, transparent 72%);
  opacity: 0.5;
  z-index: 2;
  pointer-events: none;
  animation: lampBreathe 4.5s ease-in-out infinite;
}

@keyframes lampBreathe {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.08); }
}

/* Guide text — clickable */
.guide-text {
  position: fixed;
  left: 18%;
  top: 72%;
  z-index: 3;
  margin: 0;
  font-family: var(--font-label);
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  color: rgba(252, 247, 238, 0.78);
  cursor: pointer;
  padding: 0.6rem 0.9rem;
  text-shadow: 0 1px 8px rgba(10, 14, 14, 0.5);
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out),
              transform var(--dur-fast) var(--ease-out);
}

.guide-text:hover {
  color: rgba(255, 250, 242, 0.95);
  letter-spacing: 0.2em;
  transform: translateX(3px);
}

/* Lamp hot zone */
.lamp-zone {
  position: fixed;
  left: 17%;
  top: 80%;
  width: 80px;
  height: 80px;
  margin: -40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 4;
  background: transparent;
}

/* Content wrapper — hidden until lighting, centered */
.content-wrapper {
  position: fixed;
  left: 50%;
  top: 50%;
  z-index: 2;
  width: min(560px, 84vw);
  opacity: 0;
  filter: blur(4px);
}

.content-sheet {
  width: 100%;
  max-height: 72vh;
  overflow-y: auto;
  padding: var(--space-2xl);
  background: linear-gradient(rgba(246, 238, 224, 0.42), rgba(246, 238, 224, 0.42)),
    url('@/assets/textures/paper-texture.svg');
  background-size: auto, 300px;
  border: 1px solid rgba(168, 157, 140, 0.14);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(2px);
}

.content-sheet::-webkit-scrollbar {
  width: 4px;
}
.content-sheet::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.22);
  border-radius: 2px;
}

.content-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  letter-spacing: 0.3em;
  color: var(--bark);
  margin: 0 0 0.4rem;
}

.content-title {
  font-family: var(--font-editorial);
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 400;
  color: var(--ink-dark);
  letter-spacing: 0.05em;
  margin: 0 0 var(--space-sm);
}

.content-intro {
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--ink);
  line-height: 1.8;
  margin: 0 0 var(--space-xl);
}

.project-list {
  display: flex;
  flex-direction: column;
}

.project-item {
  padding: var(--space-md) 0;
  border-top: 1px solid rgba(139, 132, 120, 0.2);
  cursor: pointer;
  transition: opacity 0.4s var(--ease-out);
}

.project-item:hover {
  opacity: 0.7;
}

.project-head {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
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
  transition: transform 0.4s var(--ease-out);
}

.project-item:hover .project-title {
  transform: translateY(-2px);
}

.project-tags {
  font-family: var(--font-label);
  font-size: 0.64rem;
  font-weight: 500;
  color: var(--ink-green);
  letter-spacing: 0.08em;
  margin: 0.15rem 0 0;
}

.project-desc {
  font-family: var(--font-body);
  font-size: 0.86rem;
  color: var(--ink);
  line-height: 1.7;
  margin: 0.5rem 0 0;
}

/* Detail panel */
.detail-panel {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 5;
  width: min(520px, 86vw);
  max-height: 78vh;
  overflow-y: auto;
  padding: var(--space-2xl);
  background: linear-gradient(rgba(246, 238, 224, 0.82), rgba(246, 238, 224, 0.82)),
    url('@/assets/textures/paper-texture.svg');
  background-size: auto, 300px;
  border: 1px solid rgba(168, 157, 140, 0.15);
  border-radius: var(--radius-lg);
  box-shadow: 0 2px 30px rgba(58, 51, 46, 0.08);
}

.detail-close {
  position: absolute;
  top: var(--space-md);
  right: var(--space-md);
  background: none;
  border: none;
  font-size: 1.3rem;
  color: var(--ink-light);
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  transition: color var(--dur-fast) var(--ease-out);
}

.detail-close:hover {
  color: var(--ink-dark);
}

.detail-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  letter-spacing: 0.24em;
  color: var(--bark);
  margin: 0 0 0.4rem;
}

.detail-title {
  font-family: var(--font-editorial);
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--ink-dark);
  letter-spacing: 0.04em;
  margin: 0 0 0.3rem;
}

.detail-tags {
  font-family: var(--font-label);
  font-size: 0.7rem;
  color: var(--ink-green);
  letter-spacing: 0.1em;
  margin: 0 0 var(--space-lg);
}

.detail-fields {
  margin: 0;
}

.detail-field {
  padding: var(--space-sm) 0;
  border-top: 1px solid rgba(139, 132, 120, 0.14);
}

.detail-label {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.12em;
  margin-bottom: 0.3rem;
}

.detail-value {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--ink);
  line-height: 1.8;
  margin: 0;
}

.detail-enter-active,
.detail-leave-active {
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
}
.detail-enter-from,
.detail-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.96);
}

@media (max-width: 768px) {
  .content-wrapper {
    left: 50%;
    top: 52%;
    width: 88vw;
  }
  .detail-panel {
    left: 50%;
    width: 88vw;
  }
}
</style>
