<template>
  <div class="h-full flex flex-col bg-white border-r border-gray-200">
    <div class="h-16 flex items-center px-6 border-b border-gray-100">
      <span class="text-xl font-bold text-gray-900">AdminPanel</span>
    </div>
    
    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      <NuxtLink 
        to="/admin/dashboard" 
        class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="$route.path === '/admin/dashboard' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        @click="$emit('item-click')"
      >
        📊 Dashboard
      </NuxtLink>
      <NuxtLink 
        to="/admin/users" 
        class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="$route.path === '/admin/users' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        @click="$emit('item-click')"
      >
        👥 Users
      </NuxtLink>
      <NuxtLink 
        to="/admin/cards" 
        class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="$route.path === '/admin/cards' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        @click="$emit('item-click')"
      >
        📇 Cards
      </NuxtLink>
      <NuxtLink 
        to="/admin/settings" 
        class="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="$route.path === '/admin/settings' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'"
        @click="$emit('item-click')"
      >
        ⚙️ Settings
      </NuxtLink>
    </nav>

    <div class="p-4 border-t border-gray-100 space-y-2">
      <NuxtLink 
        to="/dashboard" 
        class="flex w-full items-center px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg"
        @click="$emit('item-click')"
      >
        ⬅️ Back to Dashboard
      </NuxtLink>
      <button @click="$emit('logout')" class="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg">
        🚪 Logout
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['logout', 'item-click'])
</script>
