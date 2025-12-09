
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

const ogImage = computed(() => {
  if (!card.value?.avatar_url) return ''
  if (card.value.avatar_url.startsWith('http')) return card.value.avatar_url
  return `${config.public.apiBase}${card.value.avatar_url}`
})

useHead({
  title: computed(() => card.value?.title || 'Contact Share'),
  meta: computed(() => {
    const meta = []
    
    if (card.value) {
      // Basic Description
      const desc = card.value.notes || `Contatti di ${card.value.title}`
      meta.push({ name: 'description', content: desc })

      // Open Graph / Facebook
      meta.push({ property: 'og:type', content: 'profile' })
      meta.push({ property: 'og:title', content: card.value.title })
      meta.push({ property: 'og:description', content: desc })
      meta.push({ property: 'og:url', content: publicUrl.value })
      if (ogImage.value) {
        meta.push({ property: 'og:image', content: ogImage.value })
      }

      // Twitter
      meta.push({ name: 'twitter:card', content: 'summary_large_image' })
      meta.push({ name: 'twitter:title', content: card.value.title })
      meta.push({ name: 'twitter:description', content: desc })
      if (ogImage.value) {
        meta.push({ name: 'twitter:image', content: ogImage.value })
      }

      // Robots
      if (!card.value.is_indexed) {
        meta.push({ name: 'robots', content: 'noindex' })
      }
    }
    
    return meta
  })
})
</script>
