<template>
  <div class="sheet-content">
    <p class="sheet-eyebrow">06 · 联系我</p>
    <p class="contact-intro">
      如果你想进一步了解我的项目、经历或合作方向，欢迎联系我。
    </p>
    <div class="contact-list">
      <a :href="`mailto:${store.profile.social.email}`" class="contact-row">
        <span class="row-label">邮箱</span>
        <span class="row-value">{{ store.profile.social.email }}</span>
      </a>
      <a :href="store.profile.social.github" target="_blank" rel="noopener" class="contact-row">
        <span class="row-label">GitHub</span>
        <span class="row-value">github.com</span>
      </a>
      <router-link to="/contact" class="contact-row">
        <span class="row-label">简历</span>
        <span class="row-value">查看简历</span>
      </router-link>
    </div>
    <router-link to="/contact" class="sheet-more">
      <span>联系我</span>
      <span>→</span>
    </router-link>
  </div>
</template>

<script setup>
import { useAppStore } from '../../store'

const store = useAppStore()
</script>

<style scoped>
.sheet-eyebrow {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.28em;
  margin: 0 0 var(--space-lg);
}

.contact-intro {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--ink-light);
  line-height: 1.9;
  margin: 0 0 var(--space-lg);
}

.contact-list {
  display: flex;
  flex-direction: column;
  margin-bottom: var(--space-lg);
}

.contact-row {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(139, 132, 120, 0.15);
  text-decoration: none;
  transition: opacity var(--dur-fast) var(--ease-out);
}

.contact-row:hover {
  opacity: 0.7;
}

.row-label {
  font-family: var(--font-label);
  font-size: 0.66rem;
  color: var(--bark);
  letter-spacing: 0.12em;
  min-width: 60px;
  flex-shrink: 0;
}

.row-value {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--ink);
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
