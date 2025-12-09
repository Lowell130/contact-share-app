<!-- pages/cards/new.vue -->
<template>
  <section class="flex justify-center pt-6">
    <div class="w-full max-w-4xl">
      <h1 class="text-2xl font-bold mb-4 text-center">New Card</h1>
      <CardForm v-model="form" @submit="save" />
    </div>
  </section>
</template>

<script setup>
import CardForm from '~/components/CardForm.vue'

/* 🟦 IMPORT DEL TOAST */
const { success, error: toastError } = useToast()

const form = ref({})
const { $api } = useApi()

/* 🟩 FUNZIONE DI SALVATAGGIO CON TOAST */
const save = async (payload) => {
  try {
    const c = await $api('/cards', {
      method: 'POST',
      body: payload
    })

    /* 🟢 TOAST DI SUCCESSO */
    success('Card created successfully!')

    navigateTo(`/cards/${c.id}`)
  } catch (err) {
    console.error(err)

    /* 🔴 TOAST DI ERRORE (AGGIUNTIVO) */
    toastError('Error creating card.')
  }
}
</script>
