<!-- pages/cards/new.vue -->
<template>
  <section class="flex justify-center pt-6">
    <div class="w-full max-w-4xl">
      <h1 class="text-2xl font-bold mb-4 text-center">Nuova Card</h1>
      <CardForm v-model="form" @submit="save" />
    </div>
  </section>
</template>


<script setup>
import CardForm from '~/components/CardForm.vue'
const form = ref({})
const { $api } = useApi()
const save = async (payload) => {
  const c = await $api('/cards', { method:'POST', body: payload })
  navigateTo(`/cards/${c.id}`)
}
</script>
