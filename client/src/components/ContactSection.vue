<template>
  <section id="contact" class="contact-section">
    <div class="container">
      <div class="contact-header ink-reveal">
        <p class="editorial-label">Correspondence</p>
        <h2 class="editorial-title">
          Better Call<br><em>Cathy.</em>
        </h2>
      </div>

      <div class="contact-layout">
        <!-- Form �?museum label style -->
        <div class="contact-form-wrapper museum-label ink-reveal ink-reveal-delay-1">
          <form @submit.prevent="handleSubmit">
            <div class="form-field">
              <label for="name">Name</label>
              <input id="name" v-model="form.name" type="text" required />
            </div>
            <div class="form-field">
              <label for="email">Email</label>
              <input id="email" v-model="form.email" type="email" required />
            </div>
            <div class="form-field">
              <label for="message">Message</label>
              <textarea id="message" v-model="form.message" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn-editorial" :class="{ sent: submitted }">
              <span v-if="!submitted">Send Correspondence</span>
              <span v-else>Sent &mdash; Thank You</span>
            </button>
          </form>
        </div>

        <!-- Contact info �?minimal, editorial -->
        <div class="contact-details ink-reveal ink-reveal-delay-2">
          <div class="detail-item">
            <p class="detail-label">Email</p>
            <a :href="`mailto:${store.profile.social.email}`">{{ store.profile.social.email }}</a>
          </div>
          <div class="detail-item">
            <p class="detail-label">WeChat</p>
            <span class="detail-text">{{ store.profile.social.wechat }}</span>
          </div>
          <div class="detail-item">
            <p class="detail-label">Phone</p>
            <a :href="`tel:${store.profile.social.phone.replace(/\s/g, '')}`">{{ store.profile.social.phone }}</a>
          </div>
          <div class="detail-item">
            <p class="detail-label">GitHub</p>
            <a :href="store.profile.social.github" target="_blank" rel="noopener">View repositories ↗</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useAppStore } from '../store'

const store = useAppStore()
const submitted = ref(false)
const form = ref({ name: '', email: '', message: '' })

async function handleSubmit() {
  try {
    await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
  } catch (e) { /* Demo fallback */ }
  submitted.value = true
  form.value = { name: '', email: '', message: '' }
  setTimeout(() => { submitted.value = false }, 3500)
}
</script>

<style scoped>
.contact-section {
  padding: var(--space-section) 0;
}

.contact-header {
  margin-bottom: var(--space-3xl);
  max-width: 500px;
}

.contact-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--space-3xl);
  align-items: start;
}

.contact-form-wrapper {
  max-width: 460px;
}

.form-field {
  margin-bottom: var(--space-xl);
}

.form-field label {
  display: block;
  font-family: var(--font-label);
  font-size: 0.68rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: var(--space-xs);
}

.form-field input,
.form-field textarea {
  width: 100%;
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--ink-dark);
  background: rgba(244, 237, 226, 0.5);
  border: none;
  border-bottom: 1px solid rgba(139, 132, 120, 0.2);
  padding: 0.5rem 0;
  outline: none;
  transition: border-color var(--dur-fast) var(--ease-out);
  border-radius: 0;
  resize: vertical;
}

.form-field input:focus,
.form-field textarea:focus {
  border-bottom-color: var(--ink-green);
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  padding-top: var(--space-sm);
}

.detail-item {
  padding: var(--space-md) 0;
  border-bottom: 1px solid rgba(139, 132, 120, 0.1);
}

.detail-label {
  font-family: var(--font-label);
  font-size: 0.62rem;
  color: var(--bark);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: 0.15rem;
}

.detail-item a {
  font-family: var(--font-editorial);
  font-size: 1rem;
  color: var(--ink);
  letter-spacing: 0.04em;
  transition: color var(--dur-fast) var(--ease-out);
}

.detail-item a:hover { color: var(--ink-green); }

.detail-text {
  font-family: var(--font-editorial);
  font-size: 1rem;
  color: var(--ink);
  letter-spacing: 0.04em;
}

@media (max-width: 768px) {
  .contact-layout { grid-template-columns: 1fr; gap: var(--space-2xl); }
  .contact-form-wrapper { max-width: 100%; }
  .detail-item a { overflow-wrap: anywhere; }
}
</style>
