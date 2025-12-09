
<!-- pages/c/[slug].vue -->
<template>
  <section class="max-w-2xl mx-auto">
    <div v-if="error" class="p-3 border border-red-300 bg-red-50 text-red-700 rounded">
      {{ error }}
    </div>
    <div v-else-if="!card">
      Caricamento…
    </div>
    <div v-else>
      <PublicCard :card="card" :publicUrl="publicUrl" :isOwner="isOwner" />
    </div>
  </section>
</template>

<script setup>
import PublicCard from '~/components/PublicCard.vue'

const route = useRoute()
const config = useRuntimeConfig()
const reqUrl = useRequestURL()
const { user } = useAuth()

const isOwner = computed(() => {
  if (!user.value || !card.value) return false
  return user.value.id === card.value.user_id
})

const publicUrl = computed(() => `${reqUrl.protocol}//${reqUrl.host}/c/${route.params.slug}`)

const { data: card, error: fetchError } = await useFetch(
  () => `${config.public.apiBase}/public/cards/${encodeURIComponent(route.params.slug)}`,
  {
    headers: { Accept: 'application/json' },
    key: `card-${route.params.slug}`
  }
)

const error = computed(() => {
  if (fetchError.value) return 'Impossibile caricare la card pubblica.'
  if (!card.value) return 'Card non trovata.'
  return ''
})

useHead({
  meta: computed(() => {
    if (card.value && !card.value.is_indexed) {
      return [{ name: 'robots', content: 'noindex' }]
    }
    return []
  })
})
</script>
