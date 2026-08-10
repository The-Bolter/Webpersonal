import { onMounted, onUnmounted } from 'vue'
import Lenis from 'lenis'

export function useLenis() {
  let lenis = null
  let rafId = null

  function onFrame(time) {
    if (lenis) lenis.raf(time)
    rafId = requestAnimationFrame(onFrame)
  }

  onMounted(() => {
    lenis = new Lenis({
      duration: 1.6,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      wheelMultiplier: 0.8,
      touchMultiplier: 1.5,
      infinite: false,
    })

    rafId = requestAnimationFrame(onFrame)
  })

  onUnmounted(() => {
    if (lenis) lenis.destroy()
    if (rafId) cancelAnimationFrame(rafId)
  })

  return { lenis }
}
