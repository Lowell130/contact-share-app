export default defineNuxtRouteMiddleware((to) => {
  const protectedRoutes = ['/dashboard','/cards','/analytics']
  const token = process.client ? localStorage.getItem('access_token') : null
  if (protectedRoutes.some(p => to.path.startsWith(p)) && !token) {
    return navigateTo('/login')
  }
})
