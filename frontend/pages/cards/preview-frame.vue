<template>
  <div class="min-h-screen bg-white">
    <PublicCard
      v-if="card"
      :card="card"
      :publicUrl="dummyPublicUrl"
      :isOwner="true"
    />
    <div v-else class="flex items-center justify-center min-h-screen text-gray-400 text-sm">
      Waiting for data...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const card = ref(null)
const config = useRuntimeConfig()

// Handle postMessage
const onMessage = (event) => {
  // Security check: verify origin if needed, but for self-hosted it's okay-ish
  // checking event.origin === window.location.origin is good practice
  if (event.origin !== window.location.origin) return

  if (event.data && event.data.type === 'PREVIEW_UPDATE') {
    card.value = event.data.payload
  }
}

onMounted(() => {
  window.addEventListener('message', onMessage)
  // Signal ready
  if (window.parent) {
    window.parent.postMessage({ type: 'PREVIEW_READY' }, '*')
  }
})

onUnmounted(() => {
  window.removeEventListener('message', onMessage)
})

const dummyPublicUrl = computed(() => {
  const slug = card.value?.slug || 'preview'
  return `${config.public.apiBase}/c/${slug}`
})

// Define layout: false to avoid header/footer
definePageMeta({
  layout: false
})
</script>

<style>
/* Ensure body takes full height */
body, html { height: 100%; margin: 0; }
</style>
