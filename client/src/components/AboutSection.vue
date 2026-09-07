<template>
  <section id="about" class="about-section">
    <div class="container">
      <!-- Section header — top-left, editorial style -->
      <div class="about-header ink-reveal">
        <p class="editorial-label">ABOUT / 关于我</p>
        <h2 class="about-title">我是 Catherine。</h2>
        <p class="about-lead">信息管理与信息系统专业本科生，关注 AI 产品、智能工作流与增长实践。</p>
        <p class="about-lead">从内容与运营，到产品与独立项目，我喜欢把复杂问题拆解成结构，并推动它真正落地。</p>
      </div>

      <!-- Three info cards — sparse, horizontal -->
      <div class="philosophy-row">
        <div
          v-for="(card, i) in cards"
          :key="card.title"
          class="philosophy-label-card ink-reveal"
          :class="`ink-reveal-delay-${i + 1}`"
        >
          <h3><span class="card-num">{{ card.num }}</span>{{ card.title }}</h3>
          <ul class="card-list">
            <li v-for="line in card.items" :key="line">{{ line }}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const cards = [
  { num: '01', title: '关注方向', items: ['AI 产品', '智能工作流', '增长与用户运营', '产品策划'] },
  { num: '02', title: '做事方式', items: ['观察问题', '拆解结构', '快速验证', '推进落地'] },
  { num: '03', title: '工作之外', items: ['摄影', '视觉设计', '写作与内容表达'] }
]
</script>

<style scoped>
.about-section {
  padding: var(--space-section) 0;
}

.about-header {
  margin-bottom: var(--space-3xl);
  max-width: 560px;
}

.about-header .editorial-label {
  font-size: 0.8rem;
  letter-spacing: 0.2em;
  color: var(--ink-light);
  margin-bottom: var(--space-md);
}

.about-title {
  font-family: 'Songti SC', 'SimSun', 'Noto Serif SC', 'Source Han Serif SC', serif;
  font-size: clamp(40px, 3.4vw, 52px);
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: 0.04em;
  color: var(--ink-dark);
}

.about-lead {
  margin-top: var(--space-md);
  font-size: 0.98rem;
  line-height: 1.9;
  color: var(--ink-light);
}

/* Cards — light, ink-paper restraint */
.philosophy-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-2xl);
}

.philosophy-label-card {
  max-width: 320px;
  background: rgba(240, 232, 218, 0.32);
  backdrop-filter: blur(2px);
  border: 1px solid rgba(168, 157, 140, 0.1);
  border-radius: 8px;
  padding: var(--space-xl);
  box-shadow: none;
}

.philosophy-label-card h3 {
  font-family: var(--font-editorial);
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--ink-dark);
  margin: 0 0 var(--space-md);
  letter-spacing: 0.04em;
}

.card-num {
  font-family: var(--font-label);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--bark);
  letter-spacing: 0.12em;
  margin-right: 0.6rem;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.card-list li {
  font-size: 0.9rem;
  color: var(--ink);
  line-height: 1.85;
}

@media (max-width: 768px) {
  .philosophy-row { grid-template-columns: 1fr; gap: var(--space-xl); }
}
</style>
