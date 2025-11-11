<template>
  <section v-if="card">
    <h1 class="text-2xl font-bold mb-4">Modifica Card</h1>
    <CardForm v-model="form" @submit="save" />

    <div class="mt-6 flex flex-wrap gap-3">
      <!-- vCard (privata, con Bearer) -->
      <button @click="downloadVcard" class="px-3 py-2 border">
        Scarica vCard (privata)
      </button>

      <!-- QR (privato, con Bearer) -->
      <button @click="openQr" class="px-3 py-2 border">
        QR (privato)
      </button>

      <!-- pubblico -->
      <NuxtLink :to="`/c/${card.slug}`" class="px-3 py-2 border" target="_blank">
        Apri Pubblico
      </NuxtLink>

      <!-- vCard pubblica (se la card è pubblica e consente vCard) -->
      <a
        v-if="card.is_public && card.allow_vcard"
        :href="`${apiBase}/public/cards/${card.slug}/vcard`"
        class="px-3 py-2 border"
        target="_blank"
      >
        Scarica vCard (pubblica)
      </a>
    </div>

    <p v-if="error" class="mt-4 text-red-600 text-sm">{{ error }}</p>
  </section>
</template>

<script setup>
import CardForm from '~/components/CardForm.vue'

const route = useRoute()
const { $api } = useApi()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const card = ref(null)
const form = ref({})
const error = ref('')

onMounted(async () => {
  const c = await $api(`/cards/${route.params.id}`)
  card.value = c
  form.value = c
})

const save = async (payload) => {
  error.value = ''
  try {
    await $api(`/cards/${route.params.id}`, { method: 'PUT', body: payload })
    const c = await $api(`/cards/${route.params.id}`)
    card.value = c; form.value = c
  } catch (e) {
    console.error(e)
    error.value = 'Salvataggio fallito.'
  }
}

/**
 * Scarica un blob come file.
 */
const saveBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

/**
 * vCard privata (richiede Bearer). Usiamo $fetch con responseType 'blob'
 * perché gli <a href> non mandano Authorization.
 */
const downloadVcard = async () => {
  error.value = ''
  try {
    const url = `${apiBase}/cards/${card.value.id}/vcard`
    // ofetch: puoi passare responseType: 'blob'
    const blob = await $fetch(url, {
      // forziamo la richiesta con header Authorization dal nostro composable
      headers: await buildAuthHeaders(),
      responseType: 'blob'
    })
    const filename = `${card.value.slug || 'contact'}.vcf`
    saveBlob(blob, filename)
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile scaricare la vCard privata.'
  }
}

/**
 * QR privato (richiede Bearer). Apriamo in una nuova tab il blob PNG.
 */
const openQr = async () => {
  error.value = ''
  try {
    const url = `${apiBase}/cards/${card.value.id}/qrcode`
    const blob = await $fetch(url, {
      headers: await buildAuthHeaders(),
      responseType: 'blob'
    })
    const objUrl = URL.createObjectURL(blob)
    window.open(objUrl, '_blank')
    // opzionale: revoca dopo qualche secondo
    setTimeout(() => URL.revokeObjectURL(objUrl), 5000)
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile aprire il QR privato.'
  }
}

/**
 * Costruisce gli header con Authorization come fa useApi().
 * (riutilizziamo localStorage per coerenza con useAuth/useApi)
 */
const buildAuthHeaders = async () => {
  const headers = {}
  const token = process.client ? localStorage.getItem('access_token') : null
  if (token) headers.Authorization = `Bearer ${token}`
  return headers
}
</script>
