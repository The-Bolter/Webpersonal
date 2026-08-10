<template>
  <div class="floating-card museum-label breathing" :style="floatStyle">
    <div v-if="label" class="card-label editorial-label">{{ label }}</div>
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, default: '' },
  delay: { type: Number, default: 0 },
})

const floatStyle = computed(() => ({
  animationDelay: `${props.delay}s`,
}))
</script>

<style scoped>
.floating-card {
  animation: cardFloat 7s ease-in-out infinite;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0); }
  30% { transform: translateY(-3px); }
  70% { transform: translateY(1px); }
}
</style>
