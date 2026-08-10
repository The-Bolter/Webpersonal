<template>
  <section id="hero" class="hero-section">
    <!-- Top-Left: Title — ink bleed animation -->
    <div class="hero-top-left">
      <p class="hero-label ink-bleed ink-bleed-delay-1">Curated Collection &middot; No. 01</p>
      <h1 class="hero-title ink-bleed ink-bleed-delay-2">
        Where ink<br>
        meets silence
      </h1>
      <p class="hero-desc ink-bleed ink-bleed-delay-2">
        A quiet archive of code, contemplation,<br>
        and the spaces between.
      </p>
    </div>

    <!-- Bottom-Left: Call to action -->
    <div class="hero-bottom-left ink-bleed ink-bleed-delay-3">
      <a href="#projects" class="hero-cta" @click.prevent="scrollTo('projects')">
        <span class="cta-line"></span>
        <span class="cta-text">View the Collection</span>
      </a>
    </div>

    <!-- Right-Center: Floating exhibition label -->
    <div class="hero-right-mid ink-bleed ink-bleed-delay-2">
      <FloatingCard label="On View">
        <p class="exhibition-quote">
          &ldquo;Art is the only way<br>
          to run away<br>
          without leaving home.&rdquo;
        </p>
        <p class="exhibition-attr">The Curator's Log</p>
      </FloatingCard>
    </div>

    <!-- Bottom-Right: Scroll breath indicator -->
    <div class="hero-bottom-right ink-bleed ink-bleed-delay-3">
      <div class="scroll-breath" @click="scrollTo('about')">
        <span class="scroll-word">Scroll</span>
        <div class="scroll-vertical"></div>
      </div>
    </div>

    <!-- Center: Deliberately empty — breathing space -->
    <div class="hero-void"></div>
  </section>
</template>

<script setup>
import FloatingCard from './FloatingCard.vue'

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.hero-section {
  min-height: 100vh;
  position: relative;
  display: grid;
  grid-template-rows: 1fr auto 1fr;
  grid-template-columns: 1fr 1fr;
  padding: calc(var(--nav-height) + var(--space-2xl)) var(--space-xl) var(--space-2xl);
  max-width: var(--max-width);
  margin: 0 auto;
}

/* Top-Left: Poetic title block */
.hero-top-left {
  grid-row: 1;
  grid-column: 1;
  align-self: start;
  justify-self: start;
  max-width: 480px;
}

.hero-label {
  font-family: var(--font-label);
  font-size: 0.65rem;
  font-weight: 400;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.18em;
  margin-bottom: var(--space-lg);
}

/* Ink bleed animation — blur to sharp, like ink spreading on rice paper */
.ink-bleed {
  opacity: 0;
  filter: blur(18px);
  animation: inkBleed 2.6s cubic-bezier(0.22, 0.03, 0.26, 1) forwards;
}

.ink-bleed-delay-1 { animation-delay: 0.2s; }
.ink-bleed-delay-2 { animation-delay: 0.7s; }
.ink-bleed-delay-3 { animation-delay: 1.3s; }

@keyframes inkBleed {
  0%   { opacity: 0; filter: blur(18px); transform: scale(0.97); }
  25%  { opacity: 0.25; filter: blur(12px); transform: scale(0.985); }
  55%  { opacity: 0.6; filter: blur(4px); transform: scale(0.995); }
  100% { opacity: 1; filter: blur(0); transform: scale(1); }
}

.hero-title {
  font-family: var(--font-editorial);
  font-size: clamp(2.6rem, 5vw, 4.2rem);
  font-weight: 300;
  color: var(--ink-dark);
  line-height: 1.15;
  letter-spacing: 0.02em;
  margin-bottom: var(--space-xl);
}

.hero-title em {
  color: var(--ink-green);
  font-weight: 400;
}

.hero-desc {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--ink-light);
  line-height: 1.8;
  margin: 0;
}

/* Bottom-Left: CTA action */
.hero-bottom-left {
  grid-row: 3;
  grid-column: 1;
  align-self: end;
  justify-self: start;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: var(--space-md);
  font-family: var(--font-label);
  font-size: 0.75rem;
  color: var(--ink);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  transition: gap var(--dur-base) var(--ease-out),
              color var(--dur-fast) var(--ease-out);
}

.hero-cta:hover { gap: var(--space-lg); color: var(--ink-green); }

.cta-line {
  width: 24px;
  height: 1px;
  background: var(--bark);
  transition: width var(--dur-base) var(--ease-out);
}

.hero-cta:hover .cta-line { width: 36px; }

/* Right-Center: Floating exhibition card */
.hero-right-mid {
  grid-row: 1 / span 2;
  grid-column: 2;
  align-self: center;
  justify-self: center;
  max-width: 260px;
  margin-top: -4rem;
}

.exhibition-quote {
  font-family: var(--font-editorial);
  font-size: 1.15rem;
  color: var(--ink);
  line-height: 1.65;
  margin-bottom: var(--space-md);
}

.exhibition-attr {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin: 0;
}

/* Bottom-Right: Scroll indicator */
.hero-bottom-right {
  grid-row: 3;
  grid-column: 2;
  align-self: end;
  justify-self: end;
}

.scroll-breath {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
}

.scroll-word {
  font-family: var(--font-label);
  font-size: 0.6rem;
  color: var(--ink-light);
  text-transform: uppercase;
  letter-spacing: 0.2em;
}

.scroll-vertical {
  width: 1px;
  height: 40px;
  background: rgba(139, 132, 120, 0.2);
  position: relative;
  overflow: hidden;
}

.scroll-vertical::after {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 8px;
  background: var(--bark);
  animation: scrollHint 2.4s ease-in-out infinite;
}

@keyframes scrollHint {
  0% { top: -8px; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 40px; opacity: 0; }
}

/* Center void — breathing space */
.hero-void {
  grid-row: 1 / span 2;
  grid-column: 1 / -1;
  z-index: -1;
}

/* Mobile */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto auto;
    padding: calc(var(--nav-height) + var(--space-2xl)) var(--space-lg) var(--space-xl);
    gap: var(--space-2xl);
  }

  .hero-top-left { grid-row: 1; grid-column: 1; }
  .hero-right-mid {
    grid-row: 2;
    grid-column: 1;
    justify-self: start;
    max-width: 240px;
    margin-top: 0;
  }
  .hero-bottom-left { grid-row: 3; grid-column: 1; }
  .hero-bottom-right { grid-row: 4; grid-column: 1; justify-self: start; }
  .hero-void { display: none; }
}
</style>
