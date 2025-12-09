<template>
  <header class="p-4 flex justify-between items-center">
    <NuxtLink to="/" class="font-semibold text-lg hover:text-blue-600">
      ContactShare
    </NuxtLink>

    <nav class="flex gap-3 items-center">
      <ClientOnly>
        <template v-if="isLoggedIn">
          <NuxtLink to="/dashboard" class="hover:underline">Dashboard</NuxtLink>
          <NuxtLink to="/cards" class="hover:underline">Cards</NuxtLink>
          <NuxtLink to="/account" class="hover:underline">Account</NuxtLink>
          <button
            @click="onLogout"
            class="text-white bg-dark box-border border border-transparent hover:bg-dark-strong focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-xs px-4 py-1.5 focus:outline-none ml-3"
          >
            Logout
          </button>
        </template>
        <template v-else>
          <NuxtLink
            to="/register"
            class="text-white bg-brand box-border border border-transparent hover:bg-brand-strong focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
          >
            Create your card
          </NuxtLink>
          <NuxtLink
            to="/login"
            class="text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary-soft shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
          >
            Login
          </NuxtLink>
        </template>
      </ClientOnly>
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
