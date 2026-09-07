<template>
  <canvas ref="canvasRef" class="petal-canvas" aria-hidden="true"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import petal01 from '../assets/index/petals/petal-01.png'
import petal02 from '../assets/index/petals/petal-02.png'
import petal03 from '../assets/index/petals/petal-03.png'
import petal04 from '../assets/index/petals/petal-04.png'
import { preloadImage } from '../composables/useVisualPreload'

const canvasRef = ref(null)

const PETAL_SOURCES = [petal01, petal02, petal03, petal04]
const MAX_PETALS = 18

let ctx = null
let dpr = 1
let width = 0
let height = 0
let rafId = null
let lastTime = 0
let time = 0
let images = []
let imagesReady = false
let started = false
let pendingStart = null
let particles = []
let spawnTimeouts = []
let gustTimer = null
let resizeHandler = null

function rand(min, max) {
  return min + Math.random() * (max - min)
}

function randInt(min, max) {
  return Math.floor(rand(min, max + 1))
}

function preloadImages() {
  return Promise.all(PETAL_SOURCES.map(preloadImage))
    .then((results) => results.map(({ image, status }) => status === 'loaded' ? image : null))
}

function setupCanvas() {
  const canvas = canvasRef.value
  if (!canvas) return
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  const rect = canvas.getBoundingClientRect()
  width = rect.width
  height = rect.height
  canvas.width = Math.max(1, Math.round(width * dpr))
  canvas.height = Math.max(1, Math.round(height * dpr))
  ctx = canvas.getContext('2d')
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
}

function getFlowerEls() {
  return Array.from(document.querySelectorAll('.flower'))
}

// size tier: 30% small / 55% medium / 15% large
function pickSize() {
  const r = Math.random()
  if (r < 0.3) return { w: rand(7, 10), opacity: rand(0.55, 0.72), angular: rand(0.15, 0.7) }
  if (r < 0.85) return { w: rand(10, 15), opacity: rand(0.62, 0.8), angular: rand(0.15, 0.55) }
  return { w: rand(16, 20), opacity: rand(0.68, 0.84), angular: rand(0.15, 0.3) }
}

// read live rect at the moment this petal detaches (branch keeps swaying)
function spawnFromFlower(flowerEl) {
  if (!imagesReady || particles.length >= MAX_PETALS) return
  const canvas = canvasRef.value
  if (!canvas) return

  const flowerRect = flowerEl.getBoundingClientRect()
  const canvasRect = canvas.getBoundingClientRect()
  if (!flowerRect.width || !flowerRect.height || !canvasRect.width || !canvasRect.height) return

  const x = flowerRect.left + flowerRect.width / 2 - canvasRect.left + rand(-3, 7)
  const y = flowerRect.top + flowerRect.height / 2 - canvasRect.top + rand(-2, 5)

  const { w, opacity, angular } = pickSize()
  const imageIndex = randInt(0, images.length - 1)
  const img = images[imageIndex]
  const aspect = img && img.naturalHeight ? img.naturalHeight / img.naturalWidth : 1.16
  const h = w * aspect

  particles.push({
    x,
    y,
    vx: rand(-60, -28),
    vy: rand(14, 34),
    gravity: rand(9, 17),
    rotation: rand(0, Math.PI * 2),
    angularVelocity: (Math.random() > 0.5 ? 1 : -1) * angular,
    scale: 1,
    scale0: rand(0.8, 0.9),
    opacity: opacity,
    opacity0: rand(0.45, 0.65),
    targetOpacity: opacity,
    fadeIn: rand(0.2, 0.35),
    age: 0,
    life: rand(9, 13),
    swayAmplitude: rand(8, 22),
    swaySpeed: rand(0.7, 1.5),
    phase: rand(0, Math.PI * 2),
    fadeStartRatio: rand(0.72, 0.76),
    removeLineRatio: rand(0.84, 0.87),
    imageIndex,
    w,
    h
  })
}

function scheduleNextBurst() {
  if (!started) return
  if (gustTimer) clearTimeout(gustTimer)
  gustTimer = setTimeout(() => {
    if (!started) return
    burst()
    scheduleNextBurst()
  }, rand(6, 10) * 1000)
}

function burst() {
  if (!started) return

  const occasional = Math.random() < 0.25
  const count = occasional ? randInt(12, 16) : randInt(8, 12)

  const flowers = getFlowerEls()
  if (!flowers.length) {
    scheduleNextBurst()
    return
  }

  const shuffled = [...flowers].sort(() => Math.random() - 0.5)
  const chosen = shuffled.slice(0, Math.min(shuffled.length, randInt(3, 5)))

  const duration = rand(0.9, 1.5)
  for (let i = 0; i < count; i++) {
    const delay = i * rand(0.06, 0.16)
    spawnTimeouts.push(
      setTimeout(() => {
        if (!started) return
        const flower = chosen[randInt(0, chosen.length - 1)]
        spawnFromFlower(flower)
      }, Math.min(delay, duration) * 1000)
    )
  }
}

function start(detail) {
  if (started) return
  if (!imagesReady) {
    pendingStart = detail || {}
    return
  }
  started = true
  const skipped = (detail && detail.skipped) || false
  const delay = skipped ? rand(1.2, 1.8) : rand(0.9, 1.4)
  gustTimer = setTimeout(() => {
    if (!started) return
    burst()
    scheduleNextBurst()
  }, delay * 1000)
}

function stop() {
  started = false
  if (gustTimer) clearTimeout(gustTimer)
  spawnTimeouts.forEach((t) => clearTimeout(t))
  spawnTimeouts = []
  particles = []
}

function tick(now) {
  rafId = requestAnimationFrame(tick)
  const dt = Math.min((now - lastTime) / 1000, 0.05)
  lastTime = now
  time += dt
  update(dt)
  draw()
}

function update(dt) {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]
    p.age += dt

    p.vx *= 1 - 0.3 * dt
    p.vy += p.gravity * dt
    p.x += p.vx * dt
    p.y += p.vy * dt
    p.x += Math.sin(time * p.swaySpeed + p.phase) * p.swayAmplitude * dt
    p.rotation += p.angularVelocity * dt

    // spawn fade-in: like detaching from the blossom
    if (p.age < p.fadeIn) {
      const t = p.age / p.fadeIn
      p.scale = p.scale0 + (1 - p.scale0) * t
      p.opacity = p.opacity0 + (p.targetOpacity - p.opacity0) * t
    } else {
      p.scale = 1
      p.opacity = p.targetOpacity
    }

    // lake fade-out
    const fadeStartY = height * p.fadeStartRatio
    const removeLineY = height * p.removeLineRatio
    if (p.y > fadeStartY) {
      const t = (p.y - fadeStartY) / (removeLineY - fadeStartY)
      p.opacity *= Math.max(0, 1 - t)
    }

    if (p.y > removeLineY || p.age > p.life || p.x < -80 || p.x > width + 80) {
      particles.splice(i, 1)
    }
  }
}

function draw() {
  if (!ctx) return
  ctx.clearRect(0, 0, width, height)
  for (const p of particles) {
    const img = images[p.imageIndex]
    if (!img) continue
    ctx.save()
    ctx.translate(p.x, p.y)
    ctx.rotate(p.rotation)
    ctx.scale(p.scale, p.scale)
    ctx.globalAlpha = Math.max(0, Math.min(1, p.opacity))
    ctx.drawImage(img, -p.w / 2, -p.h / 2, p.w, p.h)
    ctx.restore()
  }
  ctx.globalAlpha = 1
}

onMounted(async () => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  setupCanvas()
  resizeHandler = () => setupCanvas()
  window.addEventListener('resize', resizeHandler)

  const loaded = await preloadImages()
  images = loaded.filter(Boolean)
  imagesReady = images.length === PETAL_SOURCES.length
  if (!imagesReady) return

  lastTime = performance.now()
  rafId = requestAnimationFrame(tick)

  if (pendingStart) {
    start(pendingStart)
    pendingStart = null
  }
})

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
  if (gustTimer) clearTimeout(gustTimer)
  spawnTimeouts.forEach((t) => clearTimeout(t))
  spawnTimeouts = []
  particles = []
  started = false
  imagesReady = false
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

defineExpose({ start, stop, burst })
</script>

<style scoped>
.petal-canvas {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  display: block;
  width: 100%;
  height: 100%;
}
</style>
