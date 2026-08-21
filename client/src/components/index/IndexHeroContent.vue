<template>
  <div class="sheet-content hero-content">
    <h1 class="hero-title">从探索，到创造。</h1>
    <p class="hero-name">I'm Catherine.</p>
    <p class="hero-desc">关注 AI 产品、智能工作流与增长实践。</p>
    <p class="hero-desc hero-desc-2">这里记录我的项目、经历与成长轨迹。</p>
    <button class="hero-entry" @click="$emit('next')">
      <span class="entry-text">进入我的世界</span>
      <span class="entry-arrow">→</span>
    </button>
  </div>
</template>

<script setup>
defineEmits(['next'])
</script>

<style scoped>
.hero-content {
  text-align: center;
}

.hero-title {
  font-family: var(--font-editorial);
  font-size: clamp(2.4rem, 4.6vw, 3.6rem);
  font-weight: 500;
  color: var(--ink-dark);
  line-height: 1.3;
  letter-spacing: 0.06em;
  margin: 0 0 var(--space-md);
  text-shadow: 0 1px 14px rgba(252, 247, 238, 0.7);
}

.hero-name {
  font-family: var(--font-editorial);
  font-size: clamp(1.2rem, 2.2vw, 1.5rem);
  font-weight: 400;
  color: var(--ink);
  letter-spacing: 0.06em;
  margin: 0 0 var(--space-xl);
  text-shadow: 0 1px 12px rgba(252, 247, 238, 0.7);
}

.hero-desc {
  font-family: var(--font-body);
  font-size: 0.98rem;
  font-weight: 400;
  color: var(--ink);
  line-height: 1.9;
  margin: 0;
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.6);
}

.hero-desc-2 {
  margin-top: 0.4rem;
  margin-bottom: var(--space-xl);
}

.hero-entry {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.4rem 0;
  margin-top: 1.2rem;
}

.entry-text {
  font-family: var(--font-label);
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  color: var(--ink);
  text-shadow: 0 1px 10px rgba(252, 247, 238, 0.7);
  transition: color var(--dur-fast) var(--ease-out),
              letter-spacing var(--dur-base) var(--ease-out);
}

.entry-arrow {
  font-size: 0.9rem;
  color: var(--bark);
  transition: transform var(--dur-fast) var(--ease-out);
}

.hero-entry:hover .entry-text {
  color: var(--ink-dark);
  letter-spacing: 0.24em;
}

.hero-entry:hover .entry-arrow {
  transform: translateX(5px);
}
</style>
