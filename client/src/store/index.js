import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const activeSection = ref('hero')
  const isMenuOpen = ref(false)
  const isLoading = ref(true)

  const profile = ref({
    name: 'Catherine (Cathy)',
    bio: [
      'I craft digital spaces where code meets contemplation — interfaces that breathe, typography that whispers, and interactions that feel like turning the page of a well-loved book.',
      'Rooted in full-stack development, branching into AI and design, every project is a study in balance: logic and beauty, speed and stillness, tradition and innovation.'
    ],
    skills: [
      'Vue.js', 'React', 'Node.js', 'Python',
      'AI / LLM Integration', 'UI/UX Design',
      'Rapid Prototyping', 'Figma', 'Git / CI/CD'
    ],
    philosophy: [
      {
        title: 'Scholarship',
        text: 'Every piece is informed by the quiet hum of scholarship — in people, nature, art, across generations. Knowledge is the soil from which meaningful work grows.'
      },
      {
        title: 'Teachery',
        text: 'We reject the flat, digital aesthetic, favoring grain, depth, and the soul found in the imperfections of the handmade. The human hand leaves a mark no algorithm can replicate.'
      },
      {
        title: 'Curation',
        text: 'Not a filter, but a pathway. Each project is chosen not for the moment, but for the resonance of its relevance and the story it tells.'
      }
    ],
    social: {
      github: 'https://github.com',
      linkedin: 'https://linkedin.com',
      email: 'hello@cathy.dev'
    }
  })

  const projects = ref([
    {
      id: 1,
      title: 'Reflections in Veridian',
      description: 'An exploration of depth through traditional web technologies and modern AI interaction patterns. Built with care, layer by layer.',
      tags: ['Vue 3', 'AI Integration', 'Design Systems'],
      image: '',
      github: 'https://github.com',
      demo: 'https://example.com',
      featured: true
    },
    {
      id: 2,
      title: 'Sketch Study 904',
      description: 'A rapid prototype exploring voice-driven interfaces and ambient computing — a quick study in natural interaction.',
      tags: ['React', 'Web Speech API', 'AI'],
      image: '',
      github: 'https://github.com',
      demo: null,
      featured: false
    },
    {
      id: 3,
      title: 'Botanical Patterns',
      description: 'Generative art experiment creating organic, plant-like visualizations from code. An exercise in algorithmic beauty.',
      tags: ['Canvas API', 'Generative Art', 'TypeScript'],
      image: '',
      github: 'https://github.com',
      demo: 'https://example.com',
      featured: false
    }
  ])

  const featuredProject = computed(() => projects.value.find(p => p.featured))
  const otherProjects = computed(() => projects.value.filter(p => !p.featured))

  const resume = ref({
    pdfUrl: '#',
    sections: [
      {
        title: 'Experience',
        items: [
          {
            role: 'Frontend Developer Intern',
            company: 'TechCorp Inc.',
            period: 'Summer 2025',
            description: 'Built internal design systems with Vue 3. Improved build performance by 40%. Implemented CI/CD pipelines with automated visual regression testing.'
          },
          {
            role: 'Full Stack Developer',
            company: 'StartupLab',
            period: '2024 — 2025',
            description: 'Developed MVP products using Vue.js and Node.js. Integrated AI APIs for intelligent features. Designed and implemented database schemas.'
          }
        ]
      },
      {
        title: 'Education',
        items: [
          {
            role: 'B.S. Computer Science',
            company: 'University of Technology',
            period: '2022 — 2026',
            description: 'Focus on AI/ML, software engineering, and human-computer interaction. Senior thesis on LLM-assisted creative coding.'
          }
        ]
      }
    ]
  })

  const works = ref([
    { id: 1, title: 'Open Source Library', description: 'Lightweight utility library with 500+ GitHub stars.', category: 'code', link: 'https://github.com' },
    { id: 2, title: 'Component System', description: 'Accessible, themeable components for modern frameworks.', category: 'design', link: null },
    { id: 3, title: 'AI Chat Interface', description: 'Multi-model chat with streaming and memory.', category: 'ai', link: 'https://example.com' },
    { id: 4, title: 'Motion Studies', description: 'Micro-interactions crafted for web applications.', category: 'design', link: null },
    { id: 5, title: 'RAG Knowledge Base', description: 'Retrieval-augmented generation with citations.', category: 'ai', link: 'https://github.com' },
    { id: 6, title: 'Browser Extension', description: 'Privacy tool with 2,000+ active users.', category: 'code', link: 'https://github.com' }
  ])

  const workFilter = ref('all')
  const filteredWorks = computed(() => {
    if (workFilter.value === 'all') return works.value
    return works.value.filter(w => w.category === workFilter.value)
  })

  function setActiveSection(section) { activeSection.value = section }
  function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
  function closeMenu() { isMenuOpen.value = false }
  function finishLoading() { isLoading.value = false }

  return {
    activeSection, isMenuOpen, isLoading,
    profile, projects, resume, works,
    workFilter, filteredWorks, featuredProject, otherProjects,
    setActiveSection, toggleMenu, closeMenu, finishLoading
  }
})
