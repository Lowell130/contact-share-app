<template>
  <section>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Le tue card</h1>
      <NuxtLink to="/cards/new" class="px-3 py-2 bg-black text-white rounded hover:bg-black/80">
        + Nuova
      </NuxtLink>
    </div>

    <ul v-if="cards.length" class="space-y-2">
      <li
        v-for="c in cards"
        :key="c.id"
        class="border p-3 flex justify-between items-center rounded hover:bg-gray-50 transition"
      >
        <div>
          <p class="font-semibold">{{ c.title }}</p>
          <p class="text-sm text-gray-600">/c/{{ c.slug }}</p>
        </div>

        <div class="flex gap-2">
          <NuxtLink
            :to="`/cards/${c.id}`"
            class="px-2 py-1 border rounded hover:bg-gray-100"
          >Modifica</NuxtLink>

          <a
            :href="`/c/${c.slug}`"
            target="_blank"
            class="px-2 py-1 border rounded hover:bg-gray-100"
          >Apri pubblico</a>

          <button
            @click="confirmDelete(c)"
            class="px-2 py-1 border border-red-400 text-red-600 rounded hover:bg-red-50"
          >
            Elimina
          </button>
        </div>
      </li>
    </ul>

    <p v-else class="text-gray-500">Non hai ancora creato nessuna card.</p>

    <div v-if="loading" class="mt-4 text-sm text-gray-500">Caricamento…</div>
  </section>
</template>

<script setup>
const { $api } = useApi()
const cards = ref([])
const loading = ref(false)

const loadCards = async () => {
  loading.value = true
  try {
    cards.value = await $api('/cards')
  } catch (err) {
    console.error('Errore caricamento cards', err)
  } finally {
    loading.value = false
  }
}

const confirmDelete = async (c) => {
  const ok = confirm(`Sei sicuro di voler eliminare la card “${c.title}”?`)
  if (!ok) return

  try {
    await $api(`/cards/${c.id}`, { method: 'DELETE' })
    cards.value = cards.value.filter(x => x.id !== c.id)
  } catch (err) {
    console.error('Errore eliminazione', err)
    alert('Errore durante l’eliminazione.')
  }
}

onMounted(loadCards)
</script>
