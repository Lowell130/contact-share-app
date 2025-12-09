<template>
  <section v-if="card" class="flex justify-center pt-6">
    <div class="w-full max-w-4xl">

      <h1 class="text-2xl font-bold mb-4 text-center">Modifica Card</h1>
      <CardForm v-model="form" :cardId="card.id" @submit="save" />

      <div class="mt-6 flex flex-wrap gap-3">
        <button @click="downloadVcard" class="text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none">Scarica vCard (privata)</button>
        <button @click="openQr" class="text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none">QR (privato)</button>
        <NuxtLink :to="`/c/${card.slug}`" class="text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none" target="_blank">Apri Pubblico</NuxtLink>
        <a v-if="card.is_public && card.allow_vcard"
           :href="`${apiBase}/public/cards/${card.slug}/vcard`"
           class="text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
           target="_blank">
          Scarica vCard (pubblica)
        </a>
      </div>

      <p v-if="error" class="mt-4 text-red-600 text-sm">{{ error }}</p>
    </div>
  </section>
</template>

<script setup>
import CardForm from '~/components/CardForm.vue'
const route = useRoute()
const { $api } = useApi()
const { authHeaders } = useAuth()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

/* 🟦 IMPORT TOASTS */
const { success, error: toastError, warning } = useToast()

const card = ref(null)
const form = ref({})
const error = ref('')

const load = async () => {
  const c = await $api(`/cards/${route.params.id}`)
  card.value = c
  form.value = c
}

onMounted(load)

/* 🟩 SALVATAGGIO CON TOAST */
const save = async (payload) => {
  error.value = ''
  try {
    await $api(`/cards/${route.params.id}`, {
      method: 'PUT',
      body: payload
    })

    /* 🟢 TOAST DI SUCCESSO */
    success('Card aggiornata con successo!')

    await load()
  } catch (e) {
    console.error(e)
    error.value = 'Salvataggio fallito.'

    /* 🔴 TOAST DI ERRORE */
    toastError('Errore durante l’aggiornamento della card.')
  }
}

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

/* 🟨 vCard privata con TOAST */
const downloadVcard = async () => {
  error.value = ''
  try {
    const url = `${apiBase}/cards/${card.value.id}/vcard`
    const blob = await $fetch(url, { headers: authHeaders(), responseType: 'blob' })
    const filename = `${card.value.slug || 'contact'}.vcf`
    saveBlob(blob, filename)

    /* 🟢 SUCCESSO */
    success('vCard privata scaricata!')
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile scaricare la vCard privata.'

    /* 🔴 ERRORE */
    toastError('Errore durante il download della vCard.')
  }
}

/* 🟨 QR con TOAST */
const openQr = async () => {
  error.value = ''
  try {
    const url = `${apiBase}/cards/${card.value.id}/qrcode`
    const blob = await $fetch(url, { headers: authHeaders(), responseType: 'blob' })
    const objUrl = URL.createObjectURL(blob)
    window.open(objUrl, '_blank')
    setTimeout(() => URL.revokeObjectURL(objUrl), 5000)

    /* 🟢 SUCCESSO */
    success('QR Code aperto.')
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile aprire il QR privato.'

    /* 🔴 ERRORE */
    toastError('Errore durante la generazione del QR.')
  }
}
</script>
