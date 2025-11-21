<!-- components/AppFooter.vue -->
<template>
  <footer class="p-4 text-sm text-gray-600">
    <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
      <p>© {{ year }} Contact Share</p>
      <nav class="flex gap-4">
        <NuxtLink to="/privacy" class="hover:underline">Privacy</NuxtLink>
        <NuxtLink to="/terms" class="hover:underline">Termini</NuxtLink>
        <a href="mailto:info@example.com" class="hover:underline">Contatti</a>
      </nav>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
const year = computed(() => new Date().getFullYear())
</script>
