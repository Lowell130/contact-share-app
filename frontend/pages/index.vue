<template>
  <section class="max-w-3xl mx-auto space-y-6">
    <h1 class="text-3xl font-extrabold">Crea e condividi il tuo biglietto digitale</h1>
    <p>Link breve, QR, vCard in pochi secondi. Perfetto per freelance, micro-business, eventi.</p>
    <div v-if="!isLoggedIn" class="flex gap-3">
      <NuxtLink to="/register" class="px-4 py-2 bg-black text-white">Inizia gratis</NuxtLink>
      <NuxtLink to="/login" class="px-4 py-2 border">Accedi</NuxtLink>
    </div>
  </section>
</template>

<script setup>
const { isLoggedIn } = useAuth()
</script>
