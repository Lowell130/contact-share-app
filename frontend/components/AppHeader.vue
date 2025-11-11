<template>
  <header class="border-b p-4 flex justify-between items-center">
    <NuxtLink to="/" class="font-semibold text-lg hover:text-blue-600">
      Contact Share
    </NuxtLink>

    <nav class="flex gap-3 items-center">
      <NuxtLink to="/dashboard" class="hover:underline">Dashboard</NuxtLink>
      <NuxtLink to="/cards" class="hover:underline">Cards</NuxtLink>

      <template v-if="isLoggedIn">
        <button
          @click="onLogout"
          class="px-3 py-1 border rounded text-sm hover:bg-gray-100"
        >
          Logout
        </button>
      </template>
      <template v-else>
        <NuxtLink
          to="/login"
          class="px-3 py-1 border rounded text-sm hover:bg-gray-100"
        >
          Entra
        </NuxtLink>
      </template>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const { isLoggedIn, logout } = useAuth()

const onLogout = async () => {
  await logout()
  router.push('/login')
}
</script>
