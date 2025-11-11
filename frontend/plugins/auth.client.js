// plugins/auth.client.js
export default defineNuxtPlugin(() => {
  const { loadFromStorage } = useAuth()
  loadFromStorage()
})
