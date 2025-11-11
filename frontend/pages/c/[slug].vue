<template>
  <section class="max-w-2xl mx-auto">
    <div v-if="error" class="p-3 border border-red-300 bg-red-50 text-red-700 rounded">
      {{ error }}
    </div>
    <div v-else-if="!card">
      Caricamento…
    </div>
    <div v-else>
      <PublicCard :card="card" :publicUrl="publicUrl" />
    </div>
  </section>
</template>

<script setup>
import PublicCard from '~/components/PublicCard.vue'

const route = useRoute()
const config = useRuntimeConfig()

const card = ref(null)
const error = ref('')
const publicUrl = computed(() => `${location.origin}/c/${route.params.slug}`)

const fetchPublicCard = async () => {
  try {
    const url = `${config.public.apiBase}/public/cards/${encodeURIComponent(route.params.slug)}`
    card.value = await $fetch(url, { headers: { Accept: 'application/json' } })
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile caricare la card pubblica.'
  }
}

onMounted(fetchPublicCard)
watch(() => route.params.slug, fetchPublicCard)
</script>
