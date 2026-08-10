<template>
  <div class="ink-overlay" aria-hidden="true">
    <!-- Top-left: ink branch (subtle parallax) -->
    <div class="ink-branch-tl" ref="branchTl">
      <img
        src="@/assets/textures/ink-branch-tl.svg"
        alt=""
        class="ink-img"
        loading="eager"
      />
    </div>

    <!-- Bottom-left: ink wash diffusion -->
    <div class="ink-wash-bl" ref="washBl">
      <img
        src="@/assets/textures/ink-wash-bl.svg"
        alt=""
        class="ink-img"
        loading="eager"
      />
    </div>

    <!-- Right side: dry tree silhouette -->
    <div class="ink-tree-r" ref="treeR">
      <img
        src="@/assets/textures/ink-tree-r.svg"
        alt=""
        class="ink-img"
        loading="eager"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const branchTl = ref(null)
const washBl = ref(null)
const treeR = ref(null)

let rafId = null

function updateParallax() {
  const scrollY = window.scrollY
  const vh = window.innerHeight

  if (branchTl.value) {
    branchTl.value.style.transform = `translateY(${scrollY * 0.05}px)`
  }
  if (washBl.value) {
    washBl.value.style.transform = `translateY(${scrollY * 0.03}px)`
  }
  if (treeR.value) {
    treeR.value.style.transform = `translateY(${scrollY * 0.07}px)`
  }
  rafId = requestAnimationFrame(updateParallax)
}

onMounted(() => {
  rafId = requestAnimationFrame(updateParallax)
})

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.ink-overlay {
  position: absolute;
  inset: 0;
  z-index: 3;
  opacity: 0.4;
}

.ink-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Top-left branch — anchored to top-left corner */
.ink-branch-tl {
  position: absolute;
  top: 0;
  left: 0;
  width: min(45vw, 600px);
  height: min(50vh, 500px);
  will-change: transform;
}

/* Bottom-left ink wash — anchored to bottom-left corner */
.ink-wash-bl {
  position: absolute;
  bottom: -5%;
  left: 0;
  width: min(50vw, 600px);
  height: min(45vh, 500px);
  will-change: transform;
}

/* Right dry tree — anchored to right edge, centered vertically */
.ink-tree-r {
  position: absolute;
  right: -2%;
  top: 10%;
  width: min(28vw, 400px);
  height: min(80vh, 800px);
  will-change: transform;
}
</style>
