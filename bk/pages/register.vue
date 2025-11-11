<template>
  <div class="max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Registrati</h1>
    <form @submit.prevent="onSubmit" class="space-y-3">
      <input v-model="name" placeholder="Nome" class="border p-2 w-full" />
      <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full" required />
      <input v-model="password" type="password" placeholder="Password" class="border p-2 w-full" required />
      <button class="px-4 py-2 bg-black text-white w-full">Crea account</button>
    </form>
  </div>
</template>

<script setup>
const name = ref("")
const email = ref("")
const password = ref("")
const { register } = useAuth()
const onSubmit = async () => {
  await register(email.value, password.value, name.value)
  navigateTo('/dashboard')
}
</script>
