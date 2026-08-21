<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">03 · 我的经历</p>
    <div class="tl">
      <div v-for="t in timeline" :key="t.period" class="tl-item">
        <span class="tl-dot"></span>
        <div class="tl-body">
          <p class="tl-period">{{ t.period }}</p>
          <h3 class="tl-title">{{ t.title }}</h3>
        </div>
      </div>
    </div>
    <router-link to="/journey" class="sheet-more">
      <span>查看完整经历</span>
      <span>→</span>
    </router-link>
  </div>
</template>

<script setup>
const timeline = [
  { period: '信息管理与信息系统', title: '本科在读' },
  { period: '产品运营', title: '实习实践' },
  { period: '海外 SEO / 内容增长', title: '增长实践' },
  { period: 'AI 项目实践', title: '持续探索' }
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

.tl {
  position: relative;
  padding-left: var(--space-lg);
  margin-bottom: var(--space-lg);
  text-align: left;
}

.tl::before {
  content: '';
  position: absolute;
  left: 4px;
  top: 6px;
  bottom: 6px;
  width: 1px;
  background: rgba(139, 132, 120, 0.25);
}

.tl-item {
  position: relative;
  padding-bottom: var(--space-lg);
}

.tl-dot {
  position: absolute;
  left: calc(-1 * var(--space-lg) + 1px);
  top: 5px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--paper-light);
  border: 1px solid var(--bark);
}

.tl-period {
  font-family: var(--font-label);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--bark);
  letter-spacing: 0.12em;
  margin: 0 0 0.25rem;
  text-shadow: 0 1px 8px rgba(252, 247, 238, 0.5);
}

.tl-title {
  font-family: var(--font-editorial);
  font-size: 1.06rem;
  font-weight: 500;
  color: var(--ink-dark);
  margin: 0;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
}

.sheet-more {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-label);
  font-size: 0.74rem;
  color: var(--ink);
  letter-spacing: 0.12em;
  text-decoration: none;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
  transition: color var(--dur-fast) var(--ease-out);
}

.sheet-more:hover {
  color: var(--ink-green);
}
</style>
