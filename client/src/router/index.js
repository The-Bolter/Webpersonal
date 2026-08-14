import { createRouter, createWebHashHistory } from 'vue-router'
import Index from '../views/Index.vue'
import Projects from '../views/Projects.vue'
import Journey from '../views/Journey.vue'
import Studio from '../views/Studio.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'

const routes = [
  { path: '/', name: 'Index', component: Index },
  { path: '/projects', name: 'Projects', component: Projects },
  { path: '/journey', name: 'Journey', component: Journey },
  { path: '/studio', name: 'Studio', component: Studio },
  { path: '/about', name: 'About', component: About },
  { path: '/contact', name: 'Contact', component: Contact }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
