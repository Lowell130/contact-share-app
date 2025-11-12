<template>
  <section class="min-h-screen flex items-center justify-center bg-gray-900 text-white p-6">
    <div class="border border-cyan-500 rounded-xl p-8 shadow-lg max-w-md w-full text-center">
      <img v-if="card.avatar_url" :src="card.avatar_url" class="w-24 h-24 rounded-full border-2 border-cyan-400 mx-auto" />
      <h1 class="text-2xl font-semibold mt-4 text-cyan-300">{{ card.title }}</h1>
      <p v-if="card.notes" class="text-gray-400 mt-2">{{ card.notes }}</p>
      <ul class="mt-4 text-left text-gray-300 space-y-1">
        <li v-for="(f,i) in visibleFields" :key="i" class="flex justify-between text-sm">
          <span>{{ f.label }}</span><span>{{ f.value }}</span>
        </li>
      </ul>
      <div class="mt-6">
        <a :href="vcardUrl" class="px-5 py-2 bg-cyan-600 hover:bg-cyan-700 rounded">💾 Scarica vCard</a>
      </div>
      <img :src="qrUrl" alt="QR" class="w-20 h-20 mx-auto mt-4" />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({ card: Object, vcardUrl: String, qrUrl: String, visibleFields: Array })
</script>
