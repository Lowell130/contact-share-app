// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to) => {
  // Evita esecuzione SSR
  if (process.server) return

  const { isLoggedIn, ready, loadFromStorage } = useAuth()

  // Inizializza dallo storage se non ancora pronto
  if (!ready.value) loadFromStorage()

  // Rotte sempre pubbliche
  const isPublic =
    to.path === '/' ||
    to.path === '/login' ||
    to.path.startsWith('/c/')

  if (isPublic) return

  // Rotte che richiedono auth (puoi estendere l'elenco)
  const protectedPrefixes = ['/dashboard', '/cards', '/analytics']
  const needsAuth = protectedPrefixes.some(p => to.path.startsWith(p))

  if (needsAuth && !isLoggedIn.value) {
    return navigateTo('/login', { replace: true })
  }
})
