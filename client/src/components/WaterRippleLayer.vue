<template>
  <div ref="layerRef" class="ripple-layer" aria-hidden="true"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import gsap from 'gsap'
import { useAppStore } from '../store'

const store = useAppStore()
const layerRef = ref(null)
let lastKey = null

function spawnRipple(x, y, strength) {
  if (!layerRef.value) return
  const el = document.createElement('div')
  el.className = 'ripple'
  el.style.left = x + '%'
  el.style.top = y + '%'
  layerRef.value.appendChild(el)

  const size = 90 + strength * 40
  el.style.width = size + 'px'
  el.style.height = size + 'px'
  el.style.marginLeft = -size / 2 + 'px'
  el.style.marginTop = -size / 2 + 'px'

  gsap.fromTo(
    el,
    { scale: 0.2, opacity: 0.3 * strength },
    {
      scale: 1,
      opacity: 0,
      duration: 1.2 + strength * 0.5,
      ease: 'power1.out',
      onComplete: () => el.remove()
    }
  )
}

watch(
  () => store.ripple,
  (r) => {
    if (!r) return
    const key = r.id + r.t
    if (key === lastKey) return
    lastKey = key
    spawnRipple(r.x, r.y, r.strength)
  }
)
</script>

<style scoped>
.ripple-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, transparent 52%, rgba(255, 246, 232, 0.4) 72%, transparent 100%);
  opacity: 0;
  will-change: transform, opacity;
}
</style>
