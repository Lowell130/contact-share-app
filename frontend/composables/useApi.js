// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const { authHeaders } = useAuth()
  const { error: toastError } = useToast()

  const $api = async (path, opts = {}) => {
    const url = path.startsWith('http') ? path : `${config.public.apiBase}${path}`
    const headers = {
      ...(opts.headers || {}),
      ...authHeaders(),
    }
     try {
      return await $fetch(url, {
        ...opts,
        headers,
      })
    } catch (err) {
      if (process.client) {
        const msg =
          err?.data?.detail ||
          err?.statusMessage ||
          err?.message ||
          'Errore di comunicazione con il server.'
        toastError(msg)
      }
      throw err
    }
  }


  return { $api }
}
