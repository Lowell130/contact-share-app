// composables/useAuth.js
export const useAuth = () => {
  // Stato condiviso Nuxt (SSR-safe)
  const accessToken = useState('auth_access', () => '')
  const refreshToken = useState('auth_refresh', () => '')
  const user        = useState('auth_user',   () => null)
  const ready       = useState('auth_ready',  () => false)

  const isLoggedIn = computed(() => !!accessToken.value)

  const loadFromStorage = () => {
    if (process.client) {
      accessToken.value  = localStorage.getItem('access_token')  || ''
      refreshToken.value = localStorage.getItem('refresh_token') || ''
      const raw = localStorage.getItem('user')
      user.value = raw ? JSON.parse(raw) : null
      ready.value = true
    }
  }

  const persist = () => {
    if (!process.client) return
    if (accessToken.value)  localStorage.setItem('access_token', accessToken.value)
    else                    localStorage.removeItem('access_token')
    if (refreshToken.value) localStorage.setItem('refresh_token', refreshToken.value)
    else                    localStorage.removeItem('refresh_token')
    if (user.value)         localStorage.setItem('user', JSON.stringify(user.value))
    else                    localStorage.removeItem('user')
  }

  const setTokens = (access, refresh='') => {
    accessToken.value  = access || ''
    refreshToken.value = refresh || ''
    persist()
  }

  const setUser = (u) => {
    user.value = u || null
    persist()
  }

  const logout = async () => {
    accessToken.value = ''
    refreshToken.value = ''
    user.value = null
    persist()
  }

  // Esempio login base (email/password) via backend
  // Puoi adattare se hai già un servizio altrove
  const login = async (email, password) => {
    const config = useRuntimeConfig()
    const res = await $fetch(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: { email, password },
      headers: { 'Content-Type': 'application/json' }
    })
    // res: { access_token, refresh_token, token_type, ... }
    setTokens(res.access_token, res.refresh_token)

    // opzionale: carico profilo /me
    try {
      const me = await $fetch(`${config.public.apiBase}/me`, {
        headers: { Authorization: `Bearer ${accessToken.value}` }
      })
      setUser(me)
    } catch (_) {
      setUser(null)
    }

    return true
  }

  // Headers Authorization per fetch manuali
  const authHeaders = () => {
    if (!accessToken.value) return {}
    return { Authorization: `Bearer ${accessToken.value}` }
  }

  // Inizializzazione lato client + sync su cambi di localStorage (altre tab)
  if (process.client && !ready.value) {
    loadFromStorage()
    window.addEventListener('storage', () => loadFromStorage())
  }

  return {
    // state
    accessToken, refreshToken, user, isLoggedIn, ready,
    // actions
    login, logout, setTokens, setUser,
    // utils
    authHeaders, loadFromStorage
  }
}
