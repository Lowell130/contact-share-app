<template>
  <component
    :is="templateComponent"
    :card="card"
    :publicUrl="publicUrl"
    :vcardUrl="vcardUrl"
    :qrUrl="qrUrl"
    :visibleFields="visibleFields"
    :themeName="card.theme"
  />
</template>

<script setup>
import { computed } from 'vue'
import PublicCardModern from './PublicCardModern.vue'

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

// Now we only use Modern for everything.
// Old themes (minimal, dark, gradient) will fallback to Modern defaults.
const templateComponent = computed(() => PublicCardModern)
</script>
