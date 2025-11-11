<template>
  <section v-if="data">
    <h1 class="text-2xl font-bold mb-2">Analytics</h1>
    <p>Visite totali: <strong>{{ data.total_views }}</strong> — vCard download: <strong>{{ data.total_vcard }}</strong></p>
    <pre class="mt-4 bg-gray-50 p-3 text-xs">{{ data.last30d }}</pre>
  </section>
</template>

<script setup>
const route = useRoute()
const { $api } = useApi()
const data = ref(null)
onMounted(async () => data.value = await $api(`/analytics/cards/${route.params.id}/summary`))
</script>
