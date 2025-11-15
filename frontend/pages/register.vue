<template>
  <div class="max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Registrati</h1>

    <form @submit.prevent="onSubmit" class="space-y-3">
      <input
        v-model="name"
        placeholder="Nome"
        class="border p-2 w-full rounded"
      />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="border p-2 w-full rounded"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="border p-2 w-full rounded"
        required
      />

      <p v-if="errorMsg" class="text-sm text-red-600">
        {{ errorMsg }}
      </p>

      <button
        class="px-4 py-2 bg-black text-white w-full rounded disabled:opacity-60"
        :disabled="loading"
      >
        {{ loading ? 'Creazione account…' : 'Crea account' }}
      </button>
    </form>
  </div>
</template>

<script setup>
const name = ref('')
const email = ref('')
const password = ref('')

const loading = ref(false)
const errorMsg = ref('')

const { register } = useAuth()

const onSubmit = async () => {
  errorMsg.value = ''
  loading.value = true
  try {
    await register(email.value, password.value, name.value)
    navigateTo('/dashboard')
  } catch (err) {
    console.error('Errore registrazione', err)
    // se FastAPI manda {detail: "..."} lo mostriamo, altrimenti generico
    const detail = err?.data?.detail || err?.message
    errorMsg.value = detail || 'Registrazione non riuscita'
  } finally {
    loading.value = false
  }
}
</script>
