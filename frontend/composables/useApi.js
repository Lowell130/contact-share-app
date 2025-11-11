// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const { authHeaders } = useAuth()

  const $api = async (path, opts = {}) => {
    const url = path.startsWith('http') ? path : `${config.public.apiBase}${path}`
    const headers = {
      ...(opts.headers || {}),
      ...authHeaders(),
    }
    return await $fetch(url, {
      ...opts,
      headers
    })
  }

  return { $api }
}
