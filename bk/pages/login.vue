<template>
  <div class="max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Accedi</h1>
    <form @submit.prevent="onSubmit" class="space-y-3">
      <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full" required />
      <input v-model="password" type="password" placeholder="Password" class="border p-2 w-full" required />
      <button class="px-4 py-2 bg-black text-white w-full">Login</button>
    </form>
    <p class="mt-3 text-sm">
      Oppure <button @click="magic" class="underline">link magico</button>
    </p>
  </div>
</template>

<script setup>
const email = ref("")
const password = ref("")
const { login, fetchMe } = useAuth()
const { $api } = useApi()

const onSubmit = async () => {
  await login(email.value, password.value)
  navigateTo('/dashboard')
}
const magic = async () => {
  const r = await $api('/auth/magic/request', { method:'POST', body:{ email: email.value } })
  // DEV: usa direttamente il token restituito
  const t = r.token
  await $api('/auth/magic/confirm', { method:'POST', body:{ token: t } })
  const res = await $api('/auth/refresh', { method:'POST', body:{ token: localStorage.getItem('refresh_token') || '' } })
  localStorage.setItem('access_token', res.access_token)
  localStorage.setItem('refresh_token', res.refresh_token)
  await fetchMe()
  navigateTo('/dashboard')
}
</script>
