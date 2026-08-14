<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">05 · 关于我</p>
    <p class="about-intro">
      我是信息管理与信息系统专业学生，<br />
      正在探索产品、AI、数据与增长之间的结合。
    </p>
    <div class="about-keys">
      <span v-for="k in keys" :key="k" class="key">{{ k }}</span>
    </div>
    <p class="about-note">我喜欢研究新工具，但更喜欢把研究出来的东西真正做出来。</p>
    <router-link to="/about" class="sheet-more">
      <span>更多关于我</span>
      <span>→</span>
    </router-link>
  </div>
</template>

<script setup>
const keys = ['产品思维', 'AI 实践', '数据意识', '视觉审美', '快速学习', '动手实践']
</script>

<style scoped>
.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.28em;
  margin: 0 0 var(--space-lg);
}

.about-intro {
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--ink);
  line-height: 1.9;
  margin: 0 0 var(--space-lg);
}

.about-keys {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: var(--space-lg);
}

.key {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--ink-green);
  letter-spacing: 0.08em;
  padding: 0.2rem 0.7rem;
  border: 1px solid rgba(139, 132, 120, 0.28);
  border-radius: 999px;
}

.about-note {
  font-family: var(--font-editorial);
  font-size: 0.9rem;
  font-style: italic;
  color: var(--ink-light);
  line-height: 1.8;
  margin: 0 0 var(--space-lg);
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
