import { createRouter, createWebHashHistory } from 'vue-router'
import Index from '../views/Index.vue'

const routes = [
  { path: '/', name: 'Index', component: Index },
  { path: '/projects', name: 'Projects', component: () => import('../views/Projects.vue') },
  { path: '/journey', name: 'Journey', component: () => import('../views/Journey.vue') },
  { path: '/studio', name: 'Studio', component: () => import('../views/Studio.vue') },
  { path: '/about', name: 'About', component: () => import('../views/About.vue') },
  { path: '/contact', name: 'Contact', component: () => import('../views/Contact.vue') }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
