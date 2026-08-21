<template>
  <div class="loading-screen" :class="{ hidden: !store.isLoading }">
    <!-- Ink wandering line -->
    <svg
      class="ink-stage"
      viewBox="0 0 1200 800"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <defs>
        <!-- Soft tail blur -->
        <filter id="tail-blur" x="-80%" y="-80%" width="260%" height="260%">
          <feGaussianBlur stdDeviation="6" />
        </filter>
        <!-- Large, gentle wash blur -->
        <filter id="wash-blur" x="-120%" y="-120%" width="340%" height="340%">
          <feGaussianBlur stdDeviation="12" />
        </filter>

        <!-- Ink wash gradients — solid core dissolving to nothing -->
        <radialGradient id="wash-a" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#5b5345" stop-opacity="0.24" />
          <stop offset="42%" stop-color="#5b5345" stop-opacity="0.09" />
          <stop offset="78%" stop-color="#5b5345" stop-opacity="0.02" />
          <stop offset="100%" stop-color="#5b5345" stop-opacity="0" />
        </radialGradient>
        <radialGradient id="wash-b" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#7a6b55" stop-opacity="0.17" />
          <stop offset="40%" stop-color="#7a6b55" stop-opacity="0.06" />
          <stop offset="75%" stop-color="#7a6b55" stop-opacity="0.015" />
          <stop offset="100%" stop-color="#7a6b55" stop-opacity="0" />
        </radialGradient>
        <radialGradient id="wash-c" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#5b5345" stop-opacity="0.12" />
          <stop offset="45%" stop-color="#5b5345" stop-opacity="0.04" />
          <stop offset="100%" stop-color="#5b5345" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- Light ink tail (blurred, wider, follows the line) -->
      <g class="tail-group" filter="url(#tail-blur)">
        <path class="ink-tail" d="M -20,580 C 100,540 180,640 320,560 C 380,530 400,500 440,510" />
        <path class="ink-tail" d="M 440,510 C 520,520 600,430 700,470 C 760,490 800,430 850,450" />
        <path class="ink-tail" d="M 850,450 C 930,490 1030,410 1100,450 C 1160,485 1190,440 1220,460" />
      </g>

      <!-- Main ink line -->
      <g class="line-group">
        <path class="ink-path" d="M -20,580 C 100,540 180,640 320,560 C 380,530 400,500 440,510" />
        <path class="ink-path" d="M 440,510 C 520,520 600,430 700,470 C 760,490 800,430 850,450" />
        <path class="ink-path" d="M 850,450 C 930,490 1030,410 1100,450 C 1160,485 1190,440 1220,460" />
      </g>

      <!-- Ink wash — stains seeping into the paper along the line -->
      <g class="wash-group" filter="url(#wash-blur)">
        <circle class="ink-wash wash-1" cx="130" cy="588" r="88" fill="url(#wash-a)" />
        <circle class="ink-wash wash-2" cx="300" cy="562" r="58" fill="url(#wash-c)" />
        <circle class="ink-wash wash-3" cx="500" cy="486" r="104" fill="url(#wash-a)" />
        <circle class="ink-wash wash-4" cx="662" cy="462" r="52" fill="url(#wash-b)" />
        <circle class="ink-wash wash-5" cx="812" cy="448" r="92" fill="url(#wash-b)" />
        <circle class="ink-wash wash-6" cx="985" cy="458" r="68" fill="url(#wash-c)" />
        <circle class="ink-wash wash-7" cx="1125" cy="452" r="46" fill="url(#wash-c)" />
      </g>
    </svg>

    <!-- Text -->
    <div class="loading-text">
      <p class="loading-line line-1">Hey, I'm Catherine.</p>
      <p class="loading-line line-2">Welcome to my studio.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { useAppStore } from '../store'

const store = useAppStore()
let timeline = null

function buildTimeline() {
  const paths = document.querySelectorAll('.ink-path')
  const tails = document.querySelectorAll('.ink-tail')

  // Prepare stroke dash for hand-drawn line effect
  paths.forEach((p) => {
    const len = p.getTotalLength()
    p.style.strokeDasharray = len
    p.style.strokeDashoffset = len
  })
  tails.forEach((t) => {
    const len = t.getTotalLength()
    t.style.strokeDasharray = len
    t.style.strokeDashoffset = len
  })

  const tl = gsap.timeline({
    defaults: { ease: 'sine.inOut' },
    onComplete: () => store.finishLoading()
  })

  // Ink line — slow, even writing (~2.9s), subtle hand-drawn variation.
  // Consistent power1.inOut per segment, no sudden speed changes.
  // Segment 1 (0 → 1.1s)
  tl.to(paths[0], { strokeDashoffset: 0, duration: 1.1, ease: 'power1.inOut' }, 0)
  tl.to(tails[0], { strokeDashoffset: 0, duration: 1.1, ease: 'power1.inOut' }, 0)

  // Segment 2 (1.0 → 2.1s)
  tl.to(paths[1], { strokeDashoffset: 0, duration: 1.1, ease: 'power1.inOut' }, 1.0)
  tl.to(tails[1], { strokeDashoffset: 0, duration: 1.1, ease: 'power1.inOut' }, 1.0)

  // Segment 3 (1.95 → 2.9s)
  tl.to(paths[2], { strokeDashoffset: 0, duration: 0.95, ease: 'power1.inOut' }, 1.95)
  tl.to(tails[2], { strokeDashoffset: 0, duration: 0.95, ease: 'power1.inOut' }, 1.95)

  // Ink washes — seeping into the paper, staggered with the line
  const washSpecs = [
    { sel: '.wash-1', at: 0.4,  dur: 1.7, target: 0.9 },
    { sel: '.wash-2', at: 0.8,  dur: 1.6, target: 0.75 },
    { sel: '.wash-3', at: 1.2,  dur: 1.8, target: 1.0 },
    { sel: '.wash-4', at: 1.6,  dur: 1.6, target: 0.7 },
    { sel: '.wash-5', at: 2.0,  dur: 1.6, target: 0.85 },
    { sel: '.wash-6', at: 2.3,  dur: 1.4, target: 0.7 },
    { sel: '.wash-7', at: 2.6,  dur: 1.2, target: 0.6 }
  ]

  washSpecs.forEach((w) => {
    tl.fromTo(
      w.sel,
      { opacity: 0 },
      { opacity: w.target, duration: w.dur, ease: 'sine.out' },
      w.at
    )
  })

  // Text 1 — "Hey, I'm Catherine." starts WITH the ink line (0s).
  // Continuous fade in + gentle 12px drift up, power2.out (no overshoot).
  tl.fromTo(
    '.line-1',
    { opacity: 0, y: 12 },
    { opacity: 1, y: 0, duration: 1.9, ease: 'power2.out' },
    0
  )

  // Text 2 — "Welcome to my studio." after line-1 fully appears.
  // Continuous fade in + gentle 9px drift up (1.9 → 3.0s).
  tl.fromTo(
    '.line-2',
    { opacity: 0, y: 9 },
    { opacity: 1, y: 0, duration: 1.1, ease: 'power2.out' },
    1.9
  )

  // Text 2 completes at 3.9s — finishLoading fires right after.
  // onComplete (timeline end = 3.9s) triggers store.finishLoading().

  return tl
}

function buildReducedTimeline() {
  const tl = gsap.timeline({
    onComplete: () => store.finishLoading()
  })
  tl.fromTo('.line-1', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0.2)
  tl.fromTo('.line-2', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0.8)
  // Brief hold before finishing
  tl.to({}, { duration: 0.8 }, 1.4)
  return tl
}

onMounted(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  const start = () => {
    if (!timeline) {
      timeline = reduceMotion ? buildReducedTimeline() : buildTimeline()
    }
  }

  // Wait for web fonts before starting text animation.
  // Prevents FOUT (font swap mid-animation) which looks like stutter.
  if (document.fonts && document.fonts.ready) {
    const cap = setTimeout(start, 1000)
    document.fonts.ready.then(() => {
      clearTimeout(cap)
      start()
    })
  } else {
    start()
  }
})

onUnmounted(() => {
  if (timeline) timeline.kill()
})
</script>

<style scoped>
.loading-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--paper);
  overflow: hidden;
  transition: opacity 1s var(--ease-out), visibility 1s var(--ease-out);
}

.loading-screen.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.ink-stage {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.ink-path {
  fill: none;
  stroke: var(--ink);
  stroke-width: 1.2px;
  stroke-linecap: round;
  opacity: 0.4;
}

.ink-tail {
  fill: none;
  stroke: var(--ink);
  stroke-width: 6px;
  stroke-linecap: round;
  opacity: 0.07;
}

.ink-wash {
  opacity: 0;
}

.loading-text {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 0 var(--space-lg);
}

.loading-line {
  font-family: var(--font-editorial);
  font-weight: 300;
  color: var(--ink-dark);
  line-height: 1.5;
  letter-spacing: 0.03em;
  margin: 0;
  opacity: 0;
}

.line-1 {
  font-size: clamp(1.5rem, 3.2vw, 2.4rem);
}

.line-2 {
  font-size: clamp(0.95rem, 1.9vw, 1.3rem);
  color: var(--ink-light);
  margin-top: 0.6rem;
}
</style>
