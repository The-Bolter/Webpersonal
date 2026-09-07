<template>
  <div ref="pageRef" class="studio-page" data-lenis-prevent>
    <!-- Fixed landscape background -->
    <div class="page-bg" aria-hidden="true">
      <img :src="bgSrc" alt="" :class="{ 'is-ready': backgroundReady }" />
    </div>

    <!-- Subtle readability veil -->
    <div class="page-veil" aria-hidden="true"></div>

    <!-- Window mask: clips content to the painted window interior -->
    <div ref="maskRef" class="studio-window-mask">
      <div class="studio-scroll-area" data-lenis-prevent>
        <div class="studio-content">
          <section class="studio-archive">
            <!-- Lightweight archive header + category nav -->
            <header class="archive-header">
              <nav class="archive-categories" aria-label="作品分类">
                <button
                  v-for="c in categories"
                  :key="c.id"
                  class="category-link"
                  :class="{ active: activeCategory === c.id }"
                  :disabled="c.disabled"
                  @click="switchCategory(c.id)"
                >{{ c.label }}</button>
              </nav>
            </header>

            <!-- Category transition wrapper -->
            <transition name="category" mode="out-in">
              <!-- Photography curated display -->
              <section v-if="activeCategory === 'photography'" key="photography" class="photography-section">
                <header class="photo-heading">
                  <p class="photo-index">01 / PHOTOGRAPHY</p>
                  <h2 class="photo-title">摄影作品</h2>
                  <p class="photo-desc">以真实摄影素材为基础，整理为「暗 / 映 / 隔 / 远」四组视觉主题。</p>
                </header>

                <div class="photo-grid" :class="{ 'is-ready': categoryVisualReady }">
                  <figure
                    v-for="(p, i) in photos"
                    :key="p.id"
                    class="photo-item"
                    :class="`item-${p.id}`"
                    :style="{ '--i': i }"
                  >
                    <div class="photo-plate" @click="openFocus(photos, i)">
                      <img
                        :src="p.src"
                        :alt="`${p.number} ${p.title} / ${p.en} 摄影主视觉`"
                        :loading="i === 0 ? 'eager' : 'lazy'"
                        decoding="async"
                        :class="{ 'is-loaded': imageReady[p.id] }"
                        @load="markImageReady(p.id)"
                        @error="markImageReady(p.id)"
                      />
                    </div>
                    <figcaption class="photo-caption">
                      <span class="caption-num">{{ p.number }}</span>
                      <span class="caption-title">{{ p.title }}</span>
                      <span class="caption-en">{{ p.en }}</span>
                    </figcaption>
                  </figure>
                </div>
              </section>

              <!-- Poster & Editorial curated display -->
              <section v-else-if="activeCategory === 'poster'" key="poster" class="poster-section">
                <header class="poster-heading">
                  <p class="poster-index">02 / POSTER &amp; EDITORIAL</p>
                  <h2 class="poster-title">海报与编辑设计</h2>
                  <p class="poster-desc">包含编辑排版、艺术海报与校园视觉传播设计。</p>
                </header>

                <div class="poster-layout" :class="{ 'is-ready': categoryVisualReady }">
                  <!-- Editorial — largest anchor, left -->
                  <figure class="poster-block editorial">
                    <div class="poster-plate" @click="openFocus(posterWorks, 0)">
                      <img :src="editorialPage" alt="编辑设计主视觉" loading="eager" decoding="async" :class="{ 'is-loaded': imageReady.editorial }" @load="markImageReady('editorial')" @error="markImageReady('editorial')" />
                    </div>
                    <figcaption class="poster-caption">
                      <span class="caption-title">编辑设计</span>
                      <span class="caption-en">EDITORIAL DESIGN</span>
                    </figcaption>
                  </figure>

                  <!-- Art poster — second anchor, top right -->
                  <figure class="poster-block art">
                    <div class="poster-plate" @click="openFocus(posterWorks, 1)">
                      <img :src="artPoster" alt="艺术海报" loading="lazy" decoding="async" :class="{ 'is-loaded': imageReady.artPoster }" @load="markImageReady('artPoster')" @error="markImageReady('artPoster')" />
                    </div>
                    <figcaption class="poster-caption">
                      <span class="caption-title">艺术海报</span>
                      <span class="caption-en">ART POSTER</span>
                    </figcaption>
                  </figure>

                  <!-- Tmall series — bottom right, 3 posters -->
                  <figure class="poster-block tmall">
                    <div class="tmall-head">
                      <div class="poster-caption">
                        <span class="caption-title">天猫校园视觉系列</span>
                        <span class="caption-en">TMALL CAMPUS · 3 POSTERS</span>
                      </div>
                    </div>
                    <div class="tmall-row">
                      <div
                        v-for="(t, i) in tmallSeries"
                        :key="i"
                        class="tmall-plate"
                        :style="{ '--i': i }"
                        @click="openFocus(posterWorks, 2 + i)"
                      >
                        <img :src="t.src" :alt="`天猫校园视觉系列 ${i + 1}`" loading="lazy" decoding="async" :class="{ 'is-loaded': imageReady[`tmall-${i}`] }" @load="markImageReady(`tmall-${i}`)" @error="markImageReady(`tmall-${i}`)" />
                      </div>
                    </div>
                  </figure>
                </div>
              </section>

              <!-- Interface curated display -->
              <section v-else-if="activeCategory === 'interface'" key="interface" class="interface-section">
                <header class="interface-heading">
                  <p class="interface-index">03 / INTERFACE</p>
                  <h2 class="interface-title">界面设计</h2>
                  <p class="interface-desc">两个网页界面设计实践。</p>
                </header>

                <div class="interface-layout" :class="{ 'is-ready': categoryVisualReady }">
                  <figure
                    v-for="(w, i) in interfaceWorks"
                    :key="w.id"
                    class="interface-block"
                    :class="`ui-${i + 1}`"
                    :style="{ '--i': i }"
                  >
                    <div class="interface-plate" @click="openFocus(interfaceWorks, i)">
                      <img :src="w.src" :alt="`${w.title} 界面设计`" :loading="i === 0 ? 'eager' : 'lazy'" decoding="async" :class="{ 'is-loaded': imageReady[w.id] }" @load="markImageReady(w.id)" @error="markImageReady(w.id)" />
                    </div>
                    <figcaption class="interface-caption">
                      <span class="caption-num">{{ w.number }}</span>
                      <span class="caption-title">{{ w.title }}</span>
                      <span class="caption-en">{{ w.subtitle }}</span>
                    </figcaption>
                  </figure>
                </div>
              </section>
            </transition>
          </section>
        </div>
      </div>
    </div>

    <!-- Focus viewer — teleported to body, escapes window mask clipping -->
    <Teleport to="body">
      <transition name="focus">
        <div v-if="focusOpen" class="focus-viewer" @click.self="closeFocus" @keydown.esc="closeFocus">
          <div class="focus-backdrop" aria-hidden="true"></div>

          <button class="focus-close" @click="closeFocus" aria-label="关闭预览">×</button>

          <div class="focus-toolbar">
            <span class="focus-counter">{{ pad(focusIndex + 1) }} / {{ pad(focusWorks.length) }}</span>
            <span class="focus-caption">
              <span class="focus-title">{{ focusWorks[focusIndex]?.title }}</span>
              <span class="focus-subtitle">{{ focusWorks[focusIndex]?.subtitle }}</span>
            </span>
          </div>

          <div class="focus-stage">
            <button
              class="focus-arrow prev"
              :disabled="focusIndex === 0"
              @click="focusPrev"
              aria-label="上一张"
            >←</button>

            <div class="focus-scroll">
              <img
                :key="focusWorks[focusIndex]?.id"
                class="focus-image"
                :class="`focus-image--${imageOrient}`"
                :src="focusWorks[focusIndex]?.src"
                :alt="focusWorks[focusIndex]?.title"
                @load="onFocusImageLoad"
              />
            </div>

            <button
              class="focus-arrow next"
              :disabled="focusIndex === focusWorks.length - 1"
              @click="focusNext"
              aria-label="下一张"
            >→</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import bgSrc from '../assets/pages/studio-bg.png'
import archiveShadow from '../assets/studio/photography/archive-shadow.png'
import archiveReflection from '../assets/studio/photography/archive-reflection.png'
import archiveBetween from '../assets/studio/photography/archive-between.png'
import archiveDistant from '../assets/studio/photography/archive-distant.png'
import editorialPage from '../assets/studio/poster/editorial-page.png'
import artPoster from '../assets/studio/poster/art-poster.png'
import tmall01 from '../assets/studio/poster/tmall-campus-01.png'
import tmall02 from '../assets/studio/poster/tmall-campus-02.png'
import tmall03 from '../assets/studio/poster/tmall-campus-03.png'
import webUi01 from '../assets/studio/interface/web-ui-01.png'
import webUi02 from '../assets/studio/interface/web-ui-02.png'
import { waitForVisualGroup } from '../composables/useVisualPreload'

const pageRef = ref(null)
const maskRef = ref(null)
const activeCategory = ref('photography')
const imageReady = ref({})
const backgroundReady = ref(false)
const categoryVisualReady = ref(false)
let revealFallbackTimer = null
let isActive = true
let categoryRequest = 0

const categories = [
  { id: 'photography', label: 'Photography', disabled: false },
  { id: 'poster', label: 'Poster', disabled: false },
  { id: 'interface', label: 'Interface', disabled: false }
]

const photos = [
  { id: 'shadow', number: '01', title: '暗', subtitle: 'IN SHADOW', src: archiveShadow },
  { id: 'reflection', number: '02', title: '映', subtitle: 'REFLECTION', src: archiveReflection },
  { id: 'between', number: '03', title: '隔', subtitle: 'BETWEEN', src: archiveBetween },
  { id: 'distant', number: '04', title: '远', subtitle: 'DISTANT', src: archiveDistant }
]

const tmallSeries = [
  { src: tmall01 },
  { src: tmall02 },
  { src: tmall03 }
]

const posterWorks = [
  { id: 'editorial', title: '编辑设计', subtitle: 'EDITORIAL DESIGN', src: editorialPage },
  { id: 'art-poster', title: '艺术海报', subtitle: 'ART POSTER', src: artPoster },
  { id: 'tmall-01', title: '天猫校园 01', subtitle: 'TMALL CAMPUS', src: tmall01 },
  { id: 'tmall-02', title: '天猫校园 02', subtitle: 'TMALL CAMPUS', src: tmall02 },
  { id: 'tmall-03', title: '天猫校园 03', subtitle: 'TMALL CAMPUS', src: tmall03 }
]

const interfaceWorks = [
  { id: 'web-ui-01', number: '01', title: 'Web UI 01', subtitle: 'INTERFACE DESIGN', src: webUi01 },
  { id: 'web-ui-02', number: '02', title: 'Web UI 02', subtitle: 'INTERFACE DESIGN', src: webUi02 }
]

// ---- Focus viewer state ----
const focusOpen = ref(false)
const focusWorks = ref([])
const focusIndex = ref(0)
const imageOrient = ref('landscape')

function onFocusImageLoad(e) {
  const img = e.target
  const nw = img.naturalWidth
  const nh = img.naturalHeight
  if (!nw || !nh) return
  const ratio = nw / nh
  if (nh / nw > 2.2) imageOrient.value = 'long'
  else if (ratio < 0.85) imageOrient.value = 'portrait'
  else imageOrient.value = 'landscape'
}

function switchCategory(id) {
  if (id === activeCategory.value) return
  activeCategory.value = id
  prepareCategory(id)
}

// Each image owns its own reveal.  There is deliberately no shared preload or
// decode gate: an error (or a browser decode rejection) must never hide a page.
function markImageReady(id) {
  imageReady.value[id] = true
}

function revealAllImages() {
  ;[
    ...photos.map((photo) => photo.id),
    'editorial',
    'artPoster',
    ...tmallSeries.map((_, index) => `tmall-${index}`),
    ...interfaceWorks.map((work) => work.id)
  ].forEach(markImageReady)
}

function categorySources(category) {
  if (category === 'photography') return photos.map((photo) => photo.src)
  if (category === 'poster') return posterWorks.map((work) => work.src)
  return interfaceWorks.map((work) => work.src)
}

function prepareCategory(category) {
  const request = ++categoryRequest
  categoryVisualReady.value = false
  waitForVisualGroup(categorySources(category), 1800).then(() => {
    if (isActive && request === categoryRequest) categoryVisualReady.value = true
  })
}

function openFocus(group, index) {
  focusWorks.value = group
  focusIndex.value = index
  focusOpen.value = true
}

function closeFocus() {
  focusOpen.value = false
}

function focusPrev() {
  if (focusIndex.value > 0) focusIndex.value--
}

function focusNext() {
  if (focusIndex.value < focusWorks.value.length - 1) focusIndex.value++
}

function pad(n) {
  return String(n).padStart(2, '0')
}

function onKeydown(e) {
  if (!focusOpen.value) return
  if (e.key === 'Escape') closeFocus()
  else if (e.key === 'ArrowLeft') focusPrev()
  else if (e.key === 'ArrowRight') focusNext()
}

// Painted window interior, as fractions of the background image (1672x941).
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

  const scale = Math.max(pw / IMG_W, ph / IMG_H)
  const dispW = IMG_W * scale
  const dispH = IMG_H * scale
  const offX = (pw - dispW) / 2
  const offY = (ph - dispH) / 2

  let left = offX + WINDOW.left * dispW
  let top = offY + WINDOW.top * dispH
  let right = offX + WINDOW.right * dispW
  let bottom = offY + WINDOW.bottom * dispH

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
  window.addEventListener('keydown', onKeydown)
  document.documentElement.classList.add('studio-page-active')
  document.body.classList.add('studio-page-active')
  // A short safety release preserves the browser's native image request even
  // if an event is missed during a route transition or cache revalidation.
  revealFallbackTimer = window.setTimeout(revealAllImages, 1200)
  waitForVisualGroup([bgSrc], 1800).then(() => {
    if (isActive) backgroundReady.value = true
  })
  prepareCategory(activeCategory.value)
})

onUnmounted(() => {
  isActive = false
  if (revealFallbackTimer) window.clearTimeout(revealFallbackTimer)
  window.removeEventListener('resize', computeWindow)
  window.removeEventListener('keydown', onKeydown)
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
  opacity: 0;
  transition: opacity 0.55s ease;
}
.page-bg img.is-ready { opacity: 1; }

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
  min-height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: clamp(60px, 7.5vh, 96px) clamp(28px, 4vw, 60px) var(--space-2xl);
}

.studio-scroll-area::-webkit-scrollbar {
  width: 4px;
}
.studio-scroll-area::-webkit-scrollbar-thumb {
  background: rgba(139, 132, 120, 0.25);
  border-radius: 2px;
}

/* ---- Creative Archive ---- */
.studio-archive {
  width: 100%;
  max-width: 1280px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Lightweight header */
.archive-header {
  text-align: center;
  margin-bottom: var(--space-xs);
}

.archive-categories {
  display: flex;
  justify-content: center;
  gap: var(--space-xl);
}

.category-link {
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-label);
  font-size: 0.78rem;
  letter-spacing: 0.1em;
  color: var(--ink);
  padding: 0.2rem 0;
  border-bottom: 1px solid transparent;
  transition: color var(--dur-fast) var(--ease-out),
              border-color var(--dur-fast) var(--ease-out);
}

.category-link.active {
  color: var(--ink-dark);
  border-bottom-color: var(--bark);
}

.category-link:disabled {
  color: var(--ink-light);
  opacity: 0.5;
  cursor: default;
}

/* Category transition */
.category-enter-active,
.category-leave-active {
  transition: opacity 0.35s ease;
}
.category-enter-from,
.category-leave-to {
  opacity: 0;
}

/* ---- Shared headings ---- */
.photography-section,
.poster-section,
.interface-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.photo-heading,
.poster-heading,
.interface-heading {
  text-align: center;
  margin-bottom: var(--space-xs);
}

.photo-index,
.poster-index,
.interface-index {
  font-family: var(--font-label);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--bark);
  margin: 0 0 0.15rem;
}

.photo-title,
.poster-title,
.interface-title {
  font-family: 'Songti SC', 'SimSun', 'Noto Serif SC', 'Source Han Serif SC', serif;
  font-size: clamp(26px, 2.4vw, 36px);
  font-weight: 500;
  line-height: 1.15;
  letter-spacing: 0.06em;
  color: var(--ink-dark);
  margin: 0 0 0.2rem;
}

.photo-desc,
.poster-desc,
.interface-desc {
  font-family: var(--font-body);
  font-size: clamp(12px, 0.95vw, 14px);
  line-height: 1.6;
  color: var(--ink);
  max-width: 480px;
  margin: 0 auto;
}

/* ---- Curated asymmetric grid: portraits anchors, landscapes right column ---- */
.photo-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr 1.08fr;
  grid-template-rows: repeat(2, minmax(0, 1fr));
  gap: clamp(16px, 2vw, 28px);
  width: 100%;
  height: clamp(440px, 62vh, 680px);
  opacity: 0;
  transition: opacity 0.5s ease;
}
.photo-grid.is-ready { opacity: 1; }
.photo-grid.is-ready .photo-item { animation: none; opacity: 1; }

.photo-item {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  opacity: 0;
  animation: plate-in 0.7s var(--ease-out) both;
  animation-delay: calc(var(--i) * 0.09s);
}

@keyframes plate-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.item-shadow {
  grid-column: 1;
  grid-row: 1 / 3;
}

.item-reflection {
  grid-column: 2;
  grid-row: 1 / 3;
}

.item-between {
  grid-column: 3;
  grid-row: 1;
}

.item-distant {
  grid-column: 3;
  grid-row: 2;
}

/* frameless plate — image floats on window scene */
.photo-plate {
  position: relative;
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-in;
}

.photo-plate::before {
  content: '';
  position: absolute;
  inset: -8%;
  z-index: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at center,
    rgba(245, 238, 222, 0.2) 0%,
    rgba(245, 238, 222, 0.09) 50%,
    transparent 76%
  );
}

.photo-plate img {
  position: relative;
  z-index: 1;
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 16px, black calc(100% - 16px), transparent);
  mask-image: linear-gradient(to bottom, transparent, black 16px, black calc(100% - 16px), transparent);
  opacity: 0;
  transition: opacity 0.45s ease, transform 0.45s var(--ease-out), filter 0.45s var(--ease-out);
}

.photo-plate img.is-loaded { opacity: 1; }

.photo-item:hover .photo-plate img {
  transform: translateY(-4px);
  filter: brightness(1.04);
}

/* caption — small, layered, not a card head */
.photo-caption {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  margin-top: 0.4rem;
  padding-left: 0.2rem;
}

.caption-num {
  font-family: var(--font-label);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  color: var(--ink-light);
}

.caption-title {
  font-family: 'Songti SC', 'SimSun', 'Noto Serif SC', 'Source Han Serif SC', serif;
  font-size: clamp(16px, 1.3vw, 20px);
  font-weight: 500;
  letter-spacing: 0.1em;
  color: var(--ink-dark);
}

.caption-en {
  font-family: var(--font-label);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--bark);
  opacity: 0.68;
}

/* ---- Poster & Editorial ---- */
.poster-layout {
  display: grid;
  grid-template-columns: 0.82fr 1.18fr;
  grid-template-rows: auto auto;
  gap: clamp(18px, 2.2vw, 30px);
  width: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.poster-layout.is-ready { opacity: 1; }
.poster-layout.is-ready .poster-block,
.poster-layout.is-ready .tmall-plate { animation: none; opacity: 1; }

.poster-block {
  margin: 0;
  min-width: 0;
  opacity: 0;
  animation: plate-in 0.65s var(--ease-out) both;
}

.poster-block.editorial {
  grid-column: 1;
  grid-row: 1 / 3;
  display: flex;
  flex-direction: column;
}

.poster-block.art {
  grid-column: 2;
  grid-row: 1;
  display: flex;
  flex-direction: column;
  animation-delay: 0.14s;
}

.poster-block.tmall {
  grid-column: 2;
  grid-row: 2;
  display: flex;
  flex-direction: column;
  animation-delay: 0.28s;
}

/* frameless plate */
.poster-plate {
  position: relative;
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-in;
}

.poster-plate::before {
  content: '';
  position: absolute;
  inset: -7%;
  z-index: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at center,
    rgba(245, 238, 222, 0.2) 0%,
    rgba(245, 238, 222, 0.09) 50%,
    transparent 76%
  );
}

.poster-plate img {
  position: relative;
  z-index: 1;
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 16px, black calc(100% - 16px), transparent);
  mask-image: linear-gradient(to bottom, transparent, black 16px, black calc(100% - 16px), transparent);
  opacity: 0;
  transition: opacity 0.45s ease, transform 0.45s var(--ease-out), filter 0.45s var(--ease-out);
}

.poster-plate img.is-loaded { opacity: 1; }

/* editorial — tall, main anchor */
.poster-block.editorial .poster-plate {
  min-height: clamp(460px, 60vh, 640px);
}

/* art — landscape, second anchor */
.poster-block.art .poster-plate {
  min-height: clamp(180px, 24vh, 280px);
}

.poster-block:hover .poster-plate img {
  transform: translateY(-4px);
  filter: brightness(1.03);
}

/* poster caption */
.poster-caption {
  display: flex;
  align-items: baseline;
  gap: 0.7rem;
  margin-top: 0.4rem;
  padding-left: 0.2rem;
}

/* Tmall series */
.tmall-head {
  margin-bottom: 0.3rem;
}

.tmall-row {
  display: flex;
  gap: clamp(12px, 1.4vw, 20px);
  flex: 1 1 auto;
  min-height: 0;
  align-items: flex-start;
}

.tmall-plate {
  position: relative;
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: clamp(180px, 26vh, 300px);
  cursor: zoom-in;
  opacity: 0;
  animation: plate-in 0.55s var(--ease-out) both;
  animation-delay: calc(0.42s + var(--i) * 0.1s);
}

.tmall-plate::before {
  content: '';
  position: absolute;
  inset: -7%;
  z-index: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at center,
    rgba(245, 238, 222, 0.18) 0%,
    rgba(245, 238, 222, 0.08) 50%,
    transparent 74%
  );
}

.tmall-plate img {
  position: relative;
  z-index: 1;
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 14px, black calc(100% - 14px), transparent);
  mask-image: linear-gradient(to bottom, transparent, black 14px, black calc(100% - 14px), transparent);
  opacity: 0;
  transition: opacity 0.45s ease, transform 0.45s var(--ease-out), filter 0.45s var(--ease-out);
}

.tmall-plate img.is-loaded { opacity: 1; }

.tmall-plate:hover img {
  transform: translateY(-3px);
  filter: brightness(1.03);
}

/* ---- Interface — staggered dual dialogue, small previews ---- */
.interface-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(20px, 3vw, 40px);
  width: 100%;
  align-items: start;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.interface-layout.is-ready { opacity: 1; }
.interface-layout.is-ready .interface-block { animation: none; opacity: 1; }

.interface-block {
  margin: 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  opacity: 0;
  animation: plate-in 0.7s var(--ease-out) both;
  animation-delay: calc(var(--i) * 0.15s);
}

.interface-block.ui-1 {
  margin-left: clamp(0px, 3vw, 48px);
}

.interface-block.ui-2 {
  margin-top: clamp(36px, 6vh, 72px);
}

.interface-plate {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: clamp(300px, 42vh, 440px);
  cursor: zoom-in;
}

.interface-plate::before {
  content: '';
  position: absolute;
  inset: -7%;
  z-index: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at center,
    rgba(245, 238, 222, 0.18) 0%,
    rgba(245, 238, 222, 0.08) 50%,
    transparent 74%
  );
}

.interface-plate img {
  position: relative;
  z-index: 1;
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  opacity: 0;
  box-shadow: 0 8px 28px rgba(90, 78, 62, 0.1);
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 14px, black calc(100% - 14px), transparent);
  mask-image: linear-gradient(to bottom, transparent, black 14px, black calc(100% - 14px), transparent);
  transition: transform 0.4s var(--ease-out), opacity 0.4s var(--ease-out), filter 0.4s var(--ease-out);
}

.interface-plate img.is-loaded { opacity: 0.94; }

.interface-block:hover .interface-plate img {
  transform: scale(1.008);
  opacity: 1;
  filter: brightness(1.03);
}

.interface-caption {
  display: flex;
  align-items: baseline;
  gap: 0.7rem;
  margin-top: 0.4rem;
  padding-left: 0.2rem;
}

/* ---- Focus Viewer ---- */
.focus-viewer {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.focus-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(35, 32, 27, 0.72);
  backdrop-filter: blur(6px);
}

.focus-close {
  position: absolute;
  top: 24px;
  right: 28px;
  z-index: 3;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.8rem;
  line-height: 1;
  color: rgba(245, 238, 224, 0.9);
  transition: color 0.3s var(--ease-out), transform 0.3s var(--ease-out);
}

.focus-close:hover {
  color: #fff;
  transform: rotate(90deg);
}

.focus-toolbar {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
}

.focus-counter {
  font-family: var(--font-label);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  color: rgba(245, 238, 224, 0.75);
}

.focus-caption {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
}

.focus-title {
  font-family: 'Songti SC', 'SimSun', 'Noto Serif SC', 'Source Han Serif SC', serif;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: rgba(245, 238, 224, 0.95);
}

.focus-subtitle {
  font-family: var(--font-label);
  font-size: 0.64rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(245, 238, 224, 0.55);
}

.focus-stage {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
}

.focus-scroll {
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 88vh;
  padding: 8px 0;
}

.focus-image {
  display: block;
  max-width: min(90vw, 1500px);
  max-height: 84vh;
  width: auto;
  height: auto;
  object-fit: contain;
}

/* portrait — fit whole poster in viewport, no scroll */
.focus-image--portrait {
  max-height: 84vh;
  max-width: min(72vw, 1100px);
}

/* long screenshots — readable width, internal scroll */
.focus-image--long {
  max-height: none;
  max-width: min(88vw, 1400px);
}

.focus-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  flex-shrink: 0;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.6rem;
  line-height: 1;
  color: rgba(245, 238, 224, 0.8);
  padding: 0.5rem;
  transition: color 0.3s var(--ease-out), transform 0.3s var(--ease-out);
}

.focus-arrow.prev {
  left: clamp(20px, 4vw, 72px);
}

.focus-arrow.next {
  right: clamp(20px, 4vw, 72px);
}

.focus-arrow:hover:not(:disabled) {
  color: #fff;
}

.focus-arrow.prev:hover:not(:disabled) {
  transform: translateY(-50%) translateX(-3px);
}

.focus-arrow.next:hover:not(:disabled) {
  transform: translateY(-50%) translateX(3px);
}

.focus-arrow:disabled {
  visibility: hidden;
  pointer-events: none;
}

/* focus open animation */
.focus-enter-active,
.focus-leave-active {
  transition: opacity 0.4s ease;
}

.focus-enter-active .focus-backdrop {
  transition: opacity 0.4s ease;
}

.focus-enter-active .focus-image {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.focus-enter-from,
.focus-leave-to {
  opacity: 0;
}

.focus-enter-from .focus-backdrop,
.focus-leave-to .focus-backdrop {
  opacity: 0;
}

.focus-enter-from .focus-image {
  opacity: 0;
  transform: scale(0.985) translateY(6px);
}

/* Responsive */
@media (max-width: 1280px) {
  .photo-grid {
    grid-template-columns: 1.02fr 0.96fr 1.05fr;
    height: clamp(420px, 58vh, 600px);
  }
  .poster-layout {
    grid-template-columns: 0.85fr 1.15fr;
  }
  .interface-plate {
    height: clamp(280px, 40vh, 400px);
  }
}

@media (max-width: 1024px) {
  .photo-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto;
    height: auto;
    gap: clamp(20px, 3vh, 32px);
  }
  .item-shadow {
    grid-column: 1;
    grid-row: 1 / 3;
  }
  .item-reflection {
    grid-column: 2;
    grid-row: 1;
  }
  .item-between {
    grid-column: 2;
    grid-row: 2;
  }
  .item-distant {
    grid-column: 1 / 3;
    grid-row: 3;
  }
  .photo-plate {
    min-height: 200px;
  }
  .item-shadow .photo-plate {
    min-height: 440px;
  }
  .item-distant .photo-plate {
    min-height: 240px;
  }
  .poster-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }
  .poster-block.editorial {
    grid-column: 1;
    grid-row: 1;
  }
  .poster-block.art {
    grid-column: 1;
    grid-row: 2;
  }
  .poster-block.tmall {
    grid-column: 1;
    grid-row: 3;
  }
  .poster-block.editorial .poster-plate {
    min-height: 420px;
  }
  .tmall-row {
    flex-direction: column;
  }
  .tmall-plate {
    min-height: 260px;
  }
  .interface-layout {
    grid-template-columns: 1fr;
  }
  .interface-block.ui-1,
  .interface-block.ui-2 {
    margin-left: 0;
    margin-top: 0;
  }
  .interface-plate {
    height: clamp(280px, 36vh, 360px);
  }
}
</style>
