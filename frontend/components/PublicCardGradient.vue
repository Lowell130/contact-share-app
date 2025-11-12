<template>
  <section class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6">
    <div class="bg-white/10 backdrop-blur-xl rounded-3xl p-8 text-center text-white shadow-xl max-w-md w-full">
      <img v-if="card.avatar_url" :src="card.avatar_url" class="w-28 h-28 rounded-full mx-auto border-4 border-white/40" />
      <h1 class="text-3xl font-bold mt-4">{{ card.title }}</h1>
      <p v-if="card.notes" class="opacity-90 mt-2">{{ card.notes }}</p>
      <ul class="text-sm text-left mt-4 space-y-1">
        <li v-for="(f,i) in visibleFields" :key="i" class="flex justify-between border-b border-white/20 pb-1">
          <span class="opacity-80">{{ f.label }}</span><span class="font-medium">{{ f.value }}</span>
        </li>
      </ul>
      <div class="mt-6">
        <a :href="vcardUrl" class="px-5 py-2 bg-white/20 rounded-full hover:bg-white/30">💾 Scarica vCard</a>
      </div>
      <img :src="qrUrl" alt="QR" class="w-20 h-20 mx-auto mt-4" />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({ card: Object, vcardUrl: String, qrUrl: String, visibleFields: Array })
</script>
