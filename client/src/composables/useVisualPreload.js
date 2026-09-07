// Shared, route-local visual preloader. Identical URLs share one Image request
// in this module, and neither load, decode, nor network failures can hang a UI.
const imageTasks = new Map()

export function preloadImage(src, timeout = 1800) {
  if (!src) return Promise.resolve({ status: 'empty', image: null })
  if (imageTasks.has(src)) return imageTasks.get(src)

  const task = new Promise((resolve) => {
    const image = new Image()
    let settled = false
    let timer = null
    const finish = (status) => {
      if (settled) return
      settled = true
      if (timer) window.clearTimeout(timer)
      resolve({ status, image })
    }

    image.onload = async () => {
      if (image.decode) {
        try {
          await image.decode()
        } catch {
          // Decode rejection is browser-specific and must not block reveal.
        }
      }
      finish('loaded')
    }
    image.onerror = () => finish('error')
    timer = window.setTimeout(() => finish('timeout'), timeout)
    image.src = src
  })

  imageTasks.set(src, task)
  return task
}

export async function waitForVisualGroup(sources, timeout = 1800) {
  const tasks = sources.map((src) => preloadImage(src, timeout))
  let timer = null
  const deadline = new Promise((resolve) => {
    timer = window.setTimeout(() => resolve('timeout'), timeout)
  })
  const outcome = await Promise.race([
    Promise.allSettled(tasks).then(() => 'settled'),
    deadline
  ])
  if (timer) window.clearTimeout(timer)
  return outcome
}
