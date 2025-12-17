<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Desktop Sidebar -->
    <aside class="w-64 hidden md:block">
      <AdminSidebar @logout="onLogout" />
    </aside>

    <!-- Mobile Drawer -->
    <Teleport to="body">
      <!-- Backdrop -->
      <div 
        v-if="isMobileMenuOpen" 
        @click="isMobileMenuOpen = false"
        class="fixed inset-0 bg-black/50 z-[60] backdrop-blur-sm transition-opacity md:hidden"
      ></div>

      <!-- Sidebar in Drawer -->
      <aside 
        class="fixed top-0 left-0 bottom-0 w-64 bg-white shadow-xl z-[70] transform transition-transform duration-300 ease-in-out md:hidden"
        :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
      >
         <AdminSidebar @logout="onLogout" @item-click="isMobileMenuOpen = false" />
         <!-- Close button absolute positioned or inside sidebar if we wanted, but clicking outside closes it -->
         <button @click="isMobileMenuOpen = false" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 md:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
         </button>
      </aside>
    </Teleport>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 lg:px-8">
        <div class="flex items-center gap-4">
             <!-- Mobile Menu Trigger -->
             <button @click="isMobileMenuOpen = true" class="md:hidden p-2 -ml-2 text-gray-600 hover:text-gray-900 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
             </button>

             <h1 class="text-lg font-semibold text-gray-900">
               {{ pageTitle }}
             </h1>
        </div>
        <div class="flex items-center gap-4">
            <span class="text-sm text-gray-500 hidden sm:inline">{{ user?.email }}</span>
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
import { ref, computed } from 'vue'
import AdminSidebar from '~/components/AdminSidebar.vue'

const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()
const isMobileMenuOpen = ref(false)

const onLogout = async () => {
    isMobileMenuOpen.value = false
    await logout()
    router.push('/login')
}

const pageTitle = computed(() => {
    if (route.path.includes('users')) return 'User Management'
    if (route.path.includes('cards')) return 'Cards Overview'
    return 'Dashboard'
})
</script>
