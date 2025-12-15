export default defineNuxtRouteMiddleware((to) => {
    if (process.server) return
    const { isLoggedIn, user } = useAuth()

    if (!isLoggedIn.value) {
        return navigateTo('/login')
    }

    if (user.value?.plan !== 'admin') {
        return navigateTo('/dashboard')
    }
})
