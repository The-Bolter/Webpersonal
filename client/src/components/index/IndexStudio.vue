<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">04 · 我的方法</p>
    <div class="steps">
      <div v-for="(s, i) in steps" :key="s" class="step">
        <span class="step-num">{{ String(i + 1).padStart(2, '0') }}</span>
        <span class="step-label">{{ s }}</span>
      </div>
    </div>
    <router-link to="/studio" class="sheet-more">
      <span>了解我的工作方式</span>
      <span>→</span>
    </router-link>
  </div>
</template>

<script setup>
const steps = ['发现问题', '拆解需求', '设计方案', 'AI 辅助', 'Coding', '数据验证', '持续迭代']
</script>

<style scoped>
.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.28em;
  margin: 0 0 var(--space-lg);
}

.steps {
  display: flex;
  flex-direction: column;
  margin-bottom: var(--space-lg);
}

.step {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
  padding: 0.45rem 0;
  border-top: 1px solid rgba(139, 132, 120, 0.14);
}

.step-num {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--bark);
  letter-spacing: 0.1em;
  flex-shrink: 0;
}

.step-label {
  font-family: var(--font-editorial);
  font-size: 0.98rem;
  color: var(--ink);
  letter-spacing: 0.05em;
}

.sheet-more {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-label);
  font-size: 0.7rem;
  color: var(--ink);
  letter-spacing: 0.12em;
  text-decoration: none;
  transition: color var(--dur-fast) var(--ease-out);
}

.sheet-more:hover {
  color: var(--ink-green);
}
</style>
