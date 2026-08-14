<template>
  <div class="sheet-content hero-content">
    <p class="sheet-eyebrow">从探索，到创造。</p>
    <h1 class="sheet-title">I'm Catherine.</h1>
    <p class="sheet-desc">关注 AI 产品、智能工作流与增长实践。</p>
    <p class="sheet-desc sheet-desc-2">这里记录我的项目、经历与成长轨迹。</p>
    <button class="sheet-btn" @click="$emit('next')">快速了解我</button>
  </div>
</template>

<script setup>
defineEmits(['next'])
</script>

<style scoped>
.hero-content {
  text-align: center;
}

.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.7rem;
  color: var(--bark);
  letter-spacing: 0.3em;
  margin: 0 0 var(--space-lg);
}

.sheet-title {
  font-family: var(--font-editorial);
  font-size: clamp(1.9rem, 3.4vw, 2.6rem);
  font-weight: 300;
  color: var(--ink-dark);
  line-height: 1.35;
  letter-spacing: 0.04em;
  margin: 0 0 var(--space-lg);
}

.sheet-desc {
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--ink-light);
  line-height: 1.9;
  margin: 0;
}

.sheet-desc-2 {
  margin-top: 0.4rem;
  margin-bottom: var(--space-xl);
}

.sheet-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid rgba(139, 132, 120, 0.4);
  border-radius: 999px;
  padding: 0.55rem 1.4rem;
  cursor: pointer;
  font-family: var(--font-label);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  color: var(--ink-dark);
  margin-top: 1.2rem;
  transition: background var(--dur-fast) var(--ease-out),
              border-color var(--dur-fast) var(--ease-out);
}

.sheet-btn:hover {
  background: rgba(251, 246, 238, 0.5);
  border-color: var(--bark);
}
</style>
