<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4 text-center">
    <h1 class="text-6xl font-bold text-gray-900 mb-4">{{ error.statusCode }}</h1>
    <p class="text-xl text-gray-600 mb-8">
      {{ error.statusCode === 404 ? 'Page not found' : 'An error occurred' }}
    </p>
    <p v-if="error.statusCode === 404" class="text-gray-500 mb-8 max-w-md">
      The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
    </p>
    <NuxtLink
      to="/"
      class="px-6 py-3 bg-gray-900 text-white font-medium rounded-full hover:bg-gray-800 transition-colors"
    >
      Back to Home
    </NuxtLink>
  </div>
</template>

<script setup>
defineProps({
  error: Object
})
</script>
