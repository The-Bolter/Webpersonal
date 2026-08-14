<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">02 · 精选项目</p>
    <div class="proj-row">
      <router-link
        v-for="p in projects"
        :key="p.title"
        to="/projects"
        class="proj-item"
      >
        <h3 class="proj-title">{{ p.title }}</h3>
        <p class="proj-tags">{{ p.tags.join(' / ') }}</p>
        <p class="proj-desc">{{ p.desc }}</p>
        <span class="proj-link">查看项目 →</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
const projects = [
  { title: 'AI 情报系统', tags: ['AI', '数据', '自动化'], desc: '自动采集 AI 与游戏行业热点，完成分类、评分、筛选与 AI 分析。' },
  { title: 'KOL 建联 Agent', tags: ['AI', 'Agent', '增长'], desc: '将达人筛选、数据整理、建联分发等流程，拆解成可执行的 AI 工作流。' },
  { title: '个人知识库', tags: ['AI', '产品', '知识管理'], desc: '将分散的资料转化为可检索、可管理、持续维护的个人知识系统。' }
]
</script>

<style scoped>
.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.28em;
  margin: 0 0 var(--space-lg);
}

.proj-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
}

.proj-item {
  display: flex;
  flex-direction: column;
  padding: var(--space-md) 0;
  text-decoration: none;
  transition: opacity var(--dur-fast) var(--ease-out);
}

.proj-item:hover {
  opacity: 0.72;
}

.proj-title {
  font-family: var(--font-editorial);
  font-size: 1.05rem;
  font-weight: 400;
  color: var(--ink-dark);
  margin: 0 0 0.35rem;
}

.proj-tags {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--ink-green);
  letter-spacing: 0.1em;
  margin: 0 0 0.5rem;
}

.proj-desc {
  font-family: var(--font-body);
  font-size: 0.8rem;
  color: var(--ink-light);
  line-height: 1.7;
  margin: 0 0 var(--space-md);
  flex: 1;
}

.proj-link {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--ink);
  letter-spacing: 0.1em;
}

.proj-item:hover .proj-link {
  color: var(--ink-green);
}

@media (max-width: 768px) {
  .proj-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
