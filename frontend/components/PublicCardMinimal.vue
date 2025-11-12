<template>
  <section class="max-w-xl mx-auto text-center space-y-4">
    <div v-if="card.avatar_url" class="flex justify-center">
      <img :src="card.avatar_url" class="w-24 h-24 rounded-full object-cover" />
    </div>
    <h1 class="text-2xl font-bold">{{ card.title }}</h1>
    <p v-if="card.notes" class="text-gray-600">{{ card.notes }}</p>
    <ul class="text-left space-y-2">
      <li v-for="(f,i) in visibleFields" :key="i" class="flex gap-2">
        <strong>{{ f.label }}:</strong><span>{{ f.value }}</span>
      </li>
    </ul>
    <div class="flex gap-3 justify-center mt-4">
      <a :href="vcardUrl" class="px-3 py-2 border rounded">Scarica vCard</a>
      <img :src="qrUrl" alt="QR" class="w-20 h-20" />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({ card: Object, vcardUrl: String, qrUrl: String, visibleFields: Array })
</script>
