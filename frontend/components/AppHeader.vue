<template>
  <header class="p-4 flex justify-between items-center relative z-50 bg-white">
    <NuxtLink to="/" class="font-semibold text-lg hover:text-blue-600">
      ContactShare
    </NuxtLink>

    <!-- Desktop Nav -->
    <nav class="hidden md:flex gap-3 items-center">
      <ClientOnly>
        <template v-if="isLoggedIn">
          <NuxtLink to="/dashboard" class="hover:underline">Dashboard</NuxtLink>
          <NuxtLink to="/cards" class="hover:underline">Cards</NuxtLink>
          <NuxtLink to="/account" class="hover:underline">Account</NuxtLink>
          <NuxtLink v-if="user?.plan === 'free'" to="/upgrade" class="text-blue-600 font-bold hover:underline flex items-center gap-1">
             💎 Upgrade
          </NuxtLink>
          <NuxtLink v-if="user?.plan === 'admin'" to="/admin/dashboard" class="text-red-600 font-bold hover:underline">Admin Panel</NuxtLink>
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

    <!-- Mobile Menu Button -->
    <button @click="isMobileMenuOpen = true" class="md:hidden p-2 text-gray-600 hover:text-gray-900 focus:outline-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- Mobile Menu Drawer -->
    <Teleport to="body">
      <!-- Backdrop -->
      <div 
        v-if="isMobileMenuOpen" 
        @click="isMobileMenuOpen = false"
        class="fixed inset-0 bg-black/50 z-[60] backdrop-blur-sm transition-opacity"
      ></div>

      <!-- Drawer -->
      <aside 
        class="fixed top-0 left-0 bottom-0 w-64 bg-white shadow-xl z-[70] transform transition-transform duration-300 ease-in-out flex flex-col"
        :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
      >
        <div class="p-4 border-b flex justify-between items-center bg-gray-50">
          <span class="font-semibold text-lg text-gray-800">Menu</span>
          <button @click="isMobileMenuOpen = false" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <nav class="flex-1 overflow-y-auto py-4 px-2 space-y-1">
          <ClientOnly>
            <template v-if="isLoggedIn">
              <NuxtLink to="/dashboard" @click="isMobileMenuOpen = false" class="block px-4 py-3 rounded-lg hover:bg-gray-100 text-gray-700 font-medium">Dashboard</NuxtLink>
              <NuxtLink to="/cards" @click="isMobileMenuOpen = false" class="block px-4 py-3 rounded-lg hover:bg-gray-100 text-gray-700 font-medium">Cards</NuxtLink>
              <NuxtLink to="/account" @click="isMobileMenuOpen = false" class="block px-4 py-3 rounded-lg hover:bg-gray-100 text-gray-700 font-medium">Account</NuxtLink>
              <NuxtLink v-if="user?.plan === 'free'" to="/upgrade" @click="isMobileMenuOpen = false" class="block px-4 py-3 rounded-lg hover:bg-blue-50 text-blue-600 font-bold">
                 💎 Upgrade
              </NuxtLink>
              <NuxtLink v-if="user?.plan === 'admin'" to="/admin/dashboard" @click="isMobileMenuOpen = false" class="block px-4 py-3 rounded-lg hover:bg-red-50 text-red-600 font-bold">Admin Panel</NuxtLink>
              
              <div class="border-t border-gray-100 my-2 pt-2">
                <button
                  @click="onLogout"
                  class="w-full text-left px-4 py-3 rounded-lg hover:bg-red-50 text-red-600 font-medium flex items-center gap-2"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            </template>
            <template v-else>
              <NuxtLink
                to="/login"
                @click="isMobileMenuOpen = false"
                class="block px-4 py-3 rounded-lg hover:bg-gray-100 text-gray-700 font-medium"
              >
                Login
              </NuxtLink>
              <div class="p-4">
                <NuxtLink
                  to="/register"
                  @click="isMobileMenuOpen = false"
                  class="block w-full text-center text-white bg-brand hover:bg-brand-strong font-medium rounded-full py-3 shadow-md"
                >
                  Create your card
                </NuxtLink>
              </div>
            </template>
          </ClientOnly>
        </nav>
      </aside>
    </Teleport>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, watch } from 'vue'

const router = useRouter()
const { isLoggedIn, user, logout } = useAuth()
const isMobileMenuOpen = ref(false)

const onLogout = async () => {
  isMobileMenuOpen.value = false
  await logout()
  router.push('/login')
}

// Close menu on route change (just in case)
watch(() => router.currentRoute.value.path, () => {
  isMobileMenuOpen.value = false
})
</script>
