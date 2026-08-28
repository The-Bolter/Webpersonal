<template>
  <div ref="layerRef" class="petal-layer" aria-hidden="true"></div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import gsap from 'gsap'

const layerRef = ref(null)
const MAX_PETALS = 16
let active = new Set()

const PETAL_PATH = 'M6 0.8 C9 2.6 11 5.4 11 8.6 C11 11.6 9 13.6 6 13.6 C3 13.6 1 11.6 1 8.6 C1 5.4 3 2.6 6 0.8 Z'
const PETAL_FILLS = ['#c9948e', '#c08a85', '#bb837d']
const DEBUG_FILL = '#c03428' // 朱砂 — debug-only, high visibility

// 25% small (faster) / 55% medium / 20% large (slower)
function pickSize() {
  const r = Math.random()
  if (r < 0.25) return { w: gsap.utils.random(10, 12), speed: 0.86 }
  if (r < 0.8) return { w: gsap.utils.random(13, 16), speed: 1 }
  return { w: gsap.utils.random(17, 20), speed: 1.22 }
}

function buildSvg(w, h, fill) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svg.setAttribute('viewBox', '0 0 12 14')
  svg.setAttribute('width', w)
  svg.setAttribute('height', h)
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path')
  p.setAttribute('d', PETAL_PATH)
  p.setAttribute('fill', fill || PETAL_FILLS[Math.floor(Math.random() * PETAL_FILLS.length)])
  svg.appendChild(p)
  return svg
}

/**
 * Spawn one petal. screenX / screenY = blossom centre in viewport coordinates
 * (measured from a real anchor element on the branch), converted here into the
 * petal layer's own local pixel space so branch wind transforms never apply.
 */
function spawnFromScreen(screenX, screenY) {
  const layer = layerRef.value
  if (!layer || active.size >= MAX_PETALS) return false

  const box = layer.getBoundingClientRect()
  if (!box.width || !box.height) return false

  // slight jitter around the blossom so petals never stack on one pixel
  const localX = screenX - box.left + gsap.utils.random(-12, 5)
  const localY = screenY - box.top + gsap.utils.random(-3, 8)

  const { w, speed } = pickSize()
  const h = w * 1.16

  // --- cumulative waypoints: x strictly decreases, y strictly increases ---
  const x1 = gsap.utils.random(-30, -10)
  const x2 = gsap.utils.random(-90, -40)
  let x3 = gsap.utils.random(-180, -90)
  let y1 = gsap.utils.random(8, 20)
  let y2 = gsap.utils.random(40, 110)
  let y3 = gsap.utils.random(120, 260)

  // fade near the lake — never drift past ~86% of the viewport height
  const maxFall = Math.max(60, window.innerHeight * 0.86 - screenY)
  if (y3 > maxFall) {
    const k = maxFall / y3
    y3 = maxFall
    x3 *= gsap.utils.clamp(0.6, 1, k + 0.3)
  }
  // enforce monotonic left / down so a petal can never rise or swing back right
  x3 = Math.min(x3, x2 - 20)
  y2 = Math.min(y2, y3 * 0.62)
  y1 = Math.min(y1, y2 * 0.5)

  // gentle rotation, one direction only
  const dir = Math.random() > 0.5 ? 1 : -1
  const r1 = dir * gsap.utils.random(20, 45)
  const r2 = dir * gsap.utils.random(60, 110)
  const r3 = dir * gsap.utils.random(120, 200)

  const d1 = gsap.utils.random(0.7, 1.0) * speed
  const d2 = gsap.utils.random(1.3, 1.9) * speed
  const d3 = gsap.utils.random(1.6, 2.4) * speed
  const peak = gsap.utils.random(0.78, 0.92)

  const el = document.createElement('div')
  el.className = 'petal'
  el.style.left = localX + 'px'
  el.style.top = localY + 'px'
  el.style.width = w + 'px'
  el.style.height = h + 'px'
  el.style.marginLeft = -w / 2 + 'px'
  el.style.marginTop = -h / 2 + 'px'
  el.appendChild(buildSvg(w, h))
  layer.appendChild(el)

  const tl = gsap.timeline({
    onComplete: () => {
      el.remove()
      active.delete(tl)
    }
  })
  active.add(tl)

  tl.set(el, { x: 0, y: 0, rotation: 0, scale: 0.72, opacity: 0 })
    .to(el, { opacity: peak, scale: 1, duration: 0.35, ease: 'power1.out' }, 0)
    .to(el, { x: x1, y: y1, rotation: r1, duration: d1, ease: 'sine.out' }, 0)
    .to(el, { x: x2, y: y2, rotation: r2, duration: d2, ease: 'sine.inOut' }, d1)
    .to(el, { x: x3, y: y3, rotation: r3, duration: d3, ease: 'sine.in' }, d1 + d2)
    .to(el, { opacity: 0, duration: d3 * 0.55, ease: 'power1.in' }, d1 + d2 + d3 * 0.45)

  return true
}

/* ---- Debug: single-point origin calibration (this round only) ---- */
function addMarker(localX, localY, color, size) {
  const layer = layerRef.value
  if (!layer) return
  const m = document.createElement('div')
  m.className = 'origin-marker'
  m.style.left = localX + 'px'
  m.style.top = localY + 'px'
  m.style.width = size + 'px'
  m.style.height = size + 'px'
  m.style.marginLeft = -(size / 2) + 'px'
  m.style.marginTop = -(size / 2) + 'px'
  m.style.background = color
  m.style.boxShadow = '0 0 0 3px rgba(255,255,255,0.85)'
  layer.appendChild(m)
}

// green = true flower DOM centre (screen → layer local)
function showOriginMarker(screenX, screenY) {
  const layer = layerRef.value
  if (!layer) return
  const box = layer.getBoundingClientRect()
  if (!box.width || !box.height) return
  addMarker(screenX - box.left, screenY - box.top, '#1fa563', 8)
}

// red = final petal local coords; spawn 1 debug petal (30px, opacity 1, 4s)
function spawnDebugPetal(screenX, screenY) {
  const layer = layerRef.value
  if (!layer) return false
  const box = layer.getBoundingClientRect()
  if (!box.width || !box.height) return false

  const localX = screenX - box.left
  const localY = screenY - box.top
  addMarker(localX, localY, '#d0342c', 8)

  const w = 30
  const h = w * 1.16
  const el = document.createElement('div')
  el.className = 'petal debug'
  el.style.left = localX + 'px'
  el.style.top = localY + 'px'
  el.style.width = w + 'px'
  el.style.height = h + 'px'
  el.style.marginLeft = -(w / 2) + 'px'
  el.style.marginTop = -(h / 2) + 'px'
  el.appendChild(buildSvg(w, h, DEBUG_FILL))
  layer.appendChild(el)

  gsap.set(el, { opacity: 1 })
  gsap.to(el, {
    x: -60,
    y: 140,
    rotation: 40,
    duration: 4,
    ease: 'sine.inOut',
    onComplete: () => el.remove()
  })
  return true
}

function clearAll() {
  active.forEach((tl) => { try { tl.kill() } catch (e) {} })
  active.clear()
  if (layerRef.value) {
    layerRef.value.querySelectorAll('.petal, .origin-marker').forEach((el) => el.remove())
  }
}

onUnmounted(clearAll)

defineExpose({ spawnFromScreen, clearAll, spawnDebugPetal, showOriginMarker })
</script>

<style scoped>
.petal-layer {
  position: absolute;
  inset: 0;
  z-index: 30;
  pointer-events: none;
  overflow: visible;
}

.petal {
  position: absolute;
  will-change: transform, opacity;
  filter: drop-shadow(0 1px 2px rgba(120, 80, 70, 0.16));
}

.origin-marker {
  position: absolute;
  border-radius: 50%;
  z-index: 40;
  pointer-events: none;
}
</style>
