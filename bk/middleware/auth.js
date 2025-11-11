// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn, ready } = useAuth()

  // In SSR ready può essere false; lato client verrà valorizzato subito.
  if (!process.client) return

  // attendo che il composable legga da localStorage
  if (!ready.value) return

  // Se non loggato e non stiamo già andando al login, redirigi
  if (!isLoggedIn.value && to.path !== '/login') {
    return navigateTo('/login')
  }
})
