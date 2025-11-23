// composables/useToast.js
export const useToast = () => {
  // stato globale dei toast
  const toasts = useState('toasts', () => [])

  const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const push = (message, type = 'success', timeout = 4000) => {
    if (!process.client) return

    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`
    const toast = { id, message, type }

    toasts.value.push(toast)

    if (timeout && timeout > 0) {
      setTimeout(() => {
        remove(id)
      }, timeout)
    }
  }

  const success = (msg, timeout) => push(msg, 'success', timeout)
  const danger  = (msg, timeout) => push(msg, 'danger', timeout)
  const error   = danger // alias
  const warning = (msg, timeout) => push(msg, 'warning', timeout)

  return {
    toasts,
    push,
    success,
    danger,
    error,
    warning,
    remove,
  }
}
