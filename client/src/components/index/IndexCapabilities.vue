<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">01 · 我能做什么</p>
    <div class="cap-list">
      <div v-for="c in caps" :key="c.title" class="cap-item">
        <h3 class="cap-title">{{ c.title }}</h3>
        <p class="cap-desc">{{ c.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const caps = [
  { title: 'AI 产品', desc: 'AI 应用、Agent、自动化工作流，从需求拆解到实际落地。' },
  { title: '产品设计', desc: '用户需求、产品逻辑、信息架构，把模糊想法转化成可执行方案。' },
  { title: '数据与增长', desc: 'SEO、内容增长、数据分析，用数据发现问题并验证结果。' },
  { title: 'AI + Coding', desc: '使用 AI 辅助设计与开发，快速把想法做成真实可运行的产品。' }
]
</script>

<style scoped>
.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.72rem;
  color: var(--bark);
  letter-spacing: 0.28em;
  margin: 0 0 var(--space-xl);
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
}

.cap-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 var(--space-xl);
  text-align: left;
}

.cap-item {
  padding: var(--space-md) 0;
  border-top: 1px solid rgba(139, 132, 120, 0.2);
}

.cap-title {
  font-family: var(--font-editorial);
  font-size: 1.12rem;
  font-weight: 500;
  color: var(--ink-dark);
  margin: 0 0 0.3rem;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
}

.cap-desc {
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 400;
  color: var(--ink);
  line-height: 1.7;
  margin: 0;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.5);
}

@media (max-width: 768px) {
  .cap-list {
    grid-template-columns: 1fr;
  }
}
</style>
