<!-- pages/dashboard.vue -->
<template>
  <section>
    <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
    <p class="mb-4">Visite totali e download vCard sui tuoi biglietti.</p>
    <NuxtLink to="/cards" class="underline">Gestisci le tue card</NuxtLink>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
const { fetchMe } = useAuth()

onMounted(async () => {
  if (typeof fetchMe === 'function') {
    try {
      await fetchMe()
    } catch (err) {
      console.error('Errore durante fetchMe:', err)
    }
  }
})
</script>
