<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div class="h-16 flex items-center px-6 border-b border-gray-100">
        <span class="text-xl font-bold text-gray-900">AdminPanel</span>
      </div>
      
      <nav class="flex-1 p-4 space-y-1">
        <NuxtLink 
          to="/admin/dashboard" 
          class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="$route.path === '/admin/dashboard' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        >
          📊 Dashboard
        </NuxtLink>
        <NuxtLink 
          to="/admin/users" 
          class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="$route.path === '/admin/users' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        >
          👥 Users
        </NuxtLink>
        <NuxtLink 
          to="/admin/cards" 
          class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="$route.path === '/admin/cards' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        >
          📇 Cards
        </NuxtLink>
        <NuxtLink 
          to="/admin/settings" 
          class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="$route.path === '/admin/settings' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        >
          ⚙️ Settings
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <button @click="onLogout" class="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg">
          🚪 Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 lg:px-8">
        <div class="flex items-center gap-4">
             <!-- Mobile Menu Trigger could go here -->
             <h1 class="text-lg font-semibold text-gray-900">
               {{ pageTitle }}
             </h1>
        </div>
        <div class="flex items-center gap-4">
            <span class="text-sm text-gray-500">{{ user?.email }}</span>
            <div class="px-2 py-1 text-xs font-bold text-white bg-red-600 rounded">ADMIN</div>
        </div>
      </header>

      <main class="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const onLogout = async () => {
    await logout()
    router.push('/login')
}

const pageTitle = computed(() => {
    if (route.path.includes('users')) return 'User Management'
    if (route.path.includes('cards')) return 'Cards Overview'
    return 'Dashboard'
})
</script>
