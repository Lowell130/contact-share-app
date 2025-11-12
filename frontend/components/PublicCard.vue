<template>
  <component
    :is="templateComponent"
    :card="card"
    :vcardUrl="vcardUrl"
    :qrUrl="qrUrl"
    :visibleFields="visibleFields"
  />
</template>

<script setup>
import { computed } from 'vue'
import PublicCardMinimal from './PublicCardMinimal.vue'
import PublicCardGradient from './PublicCardGradient.vue'
import PublicCardDark from './PublicCardDark.vue'
import PublicCardFlowbite from './PublicCardFlowbite.vue'   // <-- NEW

const props = defineProps({
  card: { type: Object, required: true },
  publicUrl: { type: String, required: true }
})
const config = useRuntimeConfig()

const visibleFields = computed(() => {
  const arr = Array.isArray(props.card?.fields) ? props.card.fields : []
  return arr.filter(f => f && typeof f === 'object' && (f.visible ?? true) && (f.value ?? '') !== '')
})

const vcardUrl = computed(() =>
  `${config.public.apiBase}/public/cards/${encodeURIComponent(props.card?.slug || '')}/vcard`
)
const qrUrl = computed(() =>
  `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(props.publicUrl)}`
)

const templateComponent = computed(() => {
  const t = (props.card?.theme || '').toLowerCase()
  if (t === 'gradient') return PublicCardGradient
  if (t === 'dark') return PublicCardDark
  if (t === 'flowbite') return PublicCardFlowbite   // <-- NEW
  return PublicCardMinimal
})
</script>
