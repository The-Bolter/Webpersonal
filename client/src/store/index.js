import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const isMenuOpen = ref(false)
  const isLoading = ref(true)
  const hoveredId = ref(null)
  const ripple = ref(null)

  const profile = ref({
    name: 'Catherine (Cathy)',
    bio: [
      '我关注 AI 产品、智能工作流与增长实践，持续探索如何用产品思维解决问题，用创造力把想法真正落地。',
      '从全栈开发出发，延伸到 AI 与设计，每一个项目都在寻找逻辑与美感、速度与留白、传承与创新之间的平衡。'
    ],
    skills: [
      'Vue.js', 'React', 'Node.js', 'Python',
      'AI / LLM 集成', 'UI/UX 设计',
      '快速原型', 'Figma', 'Git / CI/CD'
    ],
    philosophy: [
      {
        title: '学习',
        text: '每一件作品都源于对人、自然、艺术与跨代际知识的安静汲取。知识是让有意义的工作得以生长的土壤。'
      },
      {
        title: '实践',
        text: '我们拒绝扁平的数字质感，偏爱颗粒、层次与手作的不完美中所蕴含的灵魂。人手留下的痕迹，是算法无法复刻的。'
      },
      {
        title: '创造',
        text: '不是筛选，而是一条路径。每个项目被选择，不是因为它属于当下，而是因为它的相关性与它讲述的故事。'
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

  function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
  function closeMenu() { isMenuOpen.value = false }
  function finishLoading() { isLoading.value = false }
  function setHovered(id) { hoveredId.value = id }
  function clearHovered() { hoveredId.value = null }
  function triggerRipple(id, x, y, strength = 1) {
    ripple.value = { id, x, y, strength, t: Date.now() }
  }

  return {
    isMenuOpen, isLoading, hoveredId, ripple,
    profile, projects, resume, works,
    workFilter, filteredWorks, featuredProject, otherProjects,
    toggleMenu, closeMenu, finishLoading,
    setHovered, clearHovered, triggerRipple
  }
})
