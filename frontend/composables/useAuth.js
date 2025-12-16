// composables/useAuth.js
export const useAuth = () => {
  const accessToken = useState('auth_access', () => '')
  const refreshToken = useState('auth_refresh', () => '')
  const user = useState('auth_user', () => null)
  const ready = useState('auth_ready', () => false)

  const isLoggedIn = computed(() => !!accessToken.value)

  const loadFromStorage = () => {
    if (process.client) {
      accessToken.value = localStorage.getItem('access_token') || ''
      refreshToken.value = localStorage.getItem('refresh_token') || ''
      const raw = localStorage.getItem('user')
      user.value = raw ? JSON.parse(raw) : null
      ready.value = true
    }
  }

  const persist = () => {
    if (!process.client) return
    if (accessToken.value) localStorage.setItem('access_token', accessToken.value)
    else localStorage.removeItem('access_token')

    if (refreshToken.value) localStorage.setItem('refresh_token', refreshToken.value)
    else localStorage.removeItem('refresh_token')

    if (user.value) localStorage.setItem('user', JSON.stringify(user.value))
    else localStorage.removeItem('user')
  }

  const setTokens = (access, refresh = '') => {
    accessToken.value = access || ''
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

  const login = async (email, password) => {
    const config = useRuntimeConfig()

    const res = await $fetch(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: { email, password },
      headers: { 'Content-Type': 'application/json' }
    })

    setTokens(res.access_token, res.refresh_token)

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

  // 🆕 REGISTRAZIONE
  const register = async (email, password, name) => {
    const config = useRuntimeConfig()

    const res = await $fetch(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      body: { email, password, name },
      headers: { 'Content-Type': 'application/json' }
    })

    // il backend ti ritorna già access_token e refresh_token
    setTokens(res.access_token, res.refresh_token)

    // provo a caricare il profilo corrente
    try {
      const me = await $fetch(`${config.public.apiBase}/me`, {
        headers: { Authorization: `Bearer ${accessToken.value}` }
      })
      setUser(me)
    } catch (_) {
      // come fallback puoi almeno salvare email+name,
      // ma se preferisci lasciamo null
      setUser({ email, name })
    }

    return true
  }

  const authHeaders = () => {
    if (!accessToken.value) return {}
    return { Authorization: `Bearer ${accessToken.value}` }
  }

  // 🆕 Refresh user data from server
  const refreshUser = async () => {
    if (!accessToken.value) return null

    const config = useRuntimeConfig()
    try {
      const me = await $fetch(`${config.public.apiBase}/me`, {
        headers: { Authorization: `Bearer ${accessToken.value}` }
      })
      setUser(me)
      return me
    } catch (e) {
      console.error('Failed to refresh user:', e)
      return null
    }
  }

  if (process.client && !ready.value) {
    loadFromStorage()
    window.addEventListener('storage', () => loadFromStorage())
  }

  return {
    accessToken,
    refreshToken,
    user,
    isLoggedIn,
    ready,
    // metodi auth
    login,
    register,   // 👈 AGGIUNTO QUI
    logout,
    refreshUser, // 🆕 AGGIUNTO
    // vari
    setTokens,
    setUser,
    authHeaders,
    loadFromStorage
  }
}
