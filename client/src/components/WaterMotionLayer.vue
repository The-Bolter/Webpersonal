<template>
  <div class="water-motion" aria-hidden="true">
    <div class="water-band band-1"></div>
    <div class="water-band band-2"></div>
  </div>
</template>

<style scoped>
.water-motion {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 22%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.water-band {
  position: absolute;
  left: -50%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 246, 232, 0.07) 22%,
    transparent 44%,
    rgba(255, 246, 232, 0.05) 66%,
    transparent 88%
  );
  background-size: 50% 100%;
  animation: waterDrift 32s linear infinite;
}

.band-2 {
  opacity: 0.7;
  animation-duration: 47s;
  animation-direction: reverse;
}

@keyframes waterDrift {
  from { transform: translateX(0); }
  to { transform: translateX(25%); }
}
</style>
