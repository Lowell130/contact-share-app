<template>
  <section class="max-w-xl mx-auto text-center space-y-4">
    <div v-if="card?.avatar_url" class="flex justify-center">
      <img :src="card.avatar_url" class="w-24 h-24 rounded-full object-cover" />
    </div>

    <h1 class="text-2xl font-bold">{{ card?.title || 'Contact' }}</h1>
    <p v-if="card?.notes" class="text-gray-600">{{ card.notes }}</p>

    <ul class="text-left space-y-2">
      <li
        v-for="(f, i) in visibleFields"
        :key="i"
        class="flex items-baseline gap-2"
      >
        <strong>{{ f.label || fallbackLabel(f.type) }}:</strong>
        <span>{{ f.value }}</span>
      </li>
    </ul>

    <div class="flex gap-3 justify-center">
      <a :href="vcardUrl" class="px-3 py-2 border">Scarica vCard</a>
      <a :href="qrUrl" target="_blank" class="px-3 py-2 border">QR</a>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  card: { type: Object, required: true },
  publicUrl: { type: String, required: true }
})

const config = useRuntimeConfig()

const visibleFields = computed(() => {
  const arr = Array.isArray(props.card?.fields) ? props.card.fields : []
  return arr
    .filter(f => f && typeof f === 'object')
    .filter(f => (f.visible ?? true) && (f.value ?? '') !== '')
})

const fallbackLabel = (t) => {
  const m = String(t || '').toLowerCase()
  if (m === 'email') return 'Email'
  if (['phone','tel','mobile'].includes(m)) return 'Telefono'
  if (['url','website','site','link'].includes(m)) return 'Sito'
  if (['company','org','organization'].includes(m)) return 'Azienda'
  if (['role','title','job'].includes(m)) return 'Ruolo'
  if (['address','addr'].includes(m)) return 'Indirizzo'
  return 'Info'
}

const vcardUrl = computed(() => {
  return `${config.public.apiBase}/public/cards/${encodeURIComponent(props.card?.slug || '')}/vcard`
})

const qrUrl = computed(() =>
  `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(props.publicUrl)}`
)
</script>
