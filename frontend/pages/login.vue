<template>
  <section class="max-w-sm mx-auto mt-10 space-y-4">
    <h1 class="text-2xl font-bold">Accedi</h1>
    <form @submit.prevent="onSubmit" class="space-y-3">
      <input v-model="email" type="email" class="border p-2 w-full" placeholder="Email" required />
      <input v-model="password" type="password" class="border p-2 w-full" placeholder="Password" required />
      <button class="px-4 py-2 bg-black text-white rounded w-full">Login</button>
    </form>
    <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
  </section>
</template>

<script setup>
const router = useRouter()
const { login } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  try {
    await login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    console.error(e)
    error.value = 'Credenziali non valide.'
  }
}
</script>
