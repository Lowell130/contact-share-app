<template>
  <div
    v-if="show"
    class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-4 shadow-lg z-50 flex flex-col sm:flex-row items-center justify-between gap-4"
  >
    <div class="text-sm text-gray-600 dark:text-gray-300">
      <p>
        We use cookies to improve your experience. By continuing to browse, you accept our
        <NuxtLink to="/privacy" class="underline hover:text-gray-900 dark:hover:text-white">Privacy Policy</NuxtLink>.
      </p>
    </div>
    <div class="flex gap-3">
      <button
        @click="accept"
        class="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-md hover:bg-gray-800 transition-colors"
      >
        Accept
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const show = ref(false)

onMounted(() => {
  const consented = localStorage.getItem('cookie_consent')
  if (!consented) {
    show.value = true
  }
})

const accept = () => {
  localStorage.setItem('cookie_consent', 'true')
  show.value = false
}
</script>
