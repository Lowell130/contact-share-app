<template>
  <section class="flex justify-center pt-6">
    <div class="w-full max-w-4xl">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">Le tue card</h1>
        <NuxtLink
          to="/cards/new"
          type="button"
          class="text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary-soft shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
        >
          + Nuova card
        </NuxtLink>
      </div>

      <ul v-if="cards.length" class="space-y-2">
        <li
          v-for="c in cards"
          :key="c.id"
          class="shadow-sm px-3 py-3 flex flex-col md:flex-row justify-between items-center rounded-base border border-default bg-white hover:bg-neutral-secondary-soft/70 transition gap-3 md:gap-0"
        >
          <!-- SINISTRA: avatar + info -->
          <div class="flex items-center gap-3 w-full md:w-auto min-w-0">
            <!-- Avatar -->
            <div
              class="relative w-12 h-12 flex-shrink-0 rounded-full overflow-hidden bg-neutral-secondary-medium ring-2 ring-default"
            >
              <img
                v-if="c.avatar_url"
                :src="c.avatar_url"
                :alt="c.title"
                class="absolute inset-0 w-full h-full object-cover"
              />
              <img
                v-else
                src="/assets/images/profile-picture-3.jpg"
                alt="Avatar"
                class="absolute inset-0 w-full h-full object-cover"
              />
            </div>

            <!-- Testo: titolo, slug, mini stats -->
            <div class="min-w-0 flex-1">
              <p class="font-semibold text-heading truncate">
                {{ c.title }}
              </p>
              <p class="text-xs text-body truncate">
                /c/{{ c.slug }}
              </p>

              <!-- Mini stats -->
              <div class="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-body">
                <span v-if="c._stats">
                  👁 {{ c._stats.views_7d }} visite 7g
                </span>
                <span v-if="c._stats">
                  📇 {{ c._stats.total_vcard }} vCard
                </span>
                <span v-if="c._stats && socialTotal(c._stats.social_clicks) > 0">
                  🔗 {{ socialTotal(c._stats.social_clicks) }} click social
                </span>

                <span v-if="c._stats === null" class="text-[11px] text-gray-400">
                  Carico statistiche…
                </span>
              </div>
            </div>
          </div>

          <!-- DESTRA: azioni -->
          <div class="flex flex-row gap-2 w-full md:w-auto justify-between md:justify-end md:ml-4">
            <!-- Modifica -->
            <NuxtLink
              :to="`/cards/${c.id}`"
              type="button"
              title="Modifica"
              class="flex-1 md:flex-none justify-center items-center text-white bg-success box-border border border-transparent hover:bg-success-strong focus:ring-4 focus:ring-success-medium shadow-xs font-medium leading-5 rounded-full text-sm p-2 md:px-4 md:py-2.5 focus:outline-none flex gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pencil"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
              <span class="hidden md:inline">Modifica</span>
            </NuxtLink>

            <!-- Apri pubblico -->
            <a
              type="button"
              :href="`/c/${c.slug}`"
              target="_blank"
              title="Apri pubblico"
              class="flex-1 md:flex-none justify-center items-center text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm p-2 md:px-4 md:py-2.5 focus:outline-none flex gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-external-link"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
              <span class="hidden md:inline">Apri pubblico</span>
            </a>

            <!-- Elimina -->
            <button
              @click="confirmDelete(c)"
              title="Elimina"
              class="flex-1 md:flex-none justify-center items-center text-white bg-danger box-border border border-transparent hover:bg-danger-strong focus:ring-4 focus:ring-danger-medium shadow-xs font-medium leading-5 rounded-full text-sm p-2 md:px-4 md:py-2.5 focus:outline-none flex gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash-2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
              <span class="hidden md:inline">Elimina</span>
            </button>

            <!-- Statistiche -->
            <NuxtLink
              :to="`/analytics/${c.id}`"
              type="button"
              title="Statistiche"
              class="flex-1 md:flex-none justify-center items-center text-white bg-brand box-border border border-transparent hover:bg-brand-strong focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-full text-sm p-2 md:px-4 md:py-2.5 focus:outline-none flex gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bar-chart-3"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>
              <span class="hidden md:inline">Statistiche</span>
            </NuxtLink>
          </div>
        </li>
      </ul>

      <p v-else class="text-gray-500">Non hai ancora creato nessuna card.</p>

      <div v-if="loading" class="mt-4 text-sm text-gray-500">
        Caricamento…
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const { $api } = useApi()
const cards = ref([])
const loading = ref(false)

/* 🟦 IMPORT TOASTS */
const { success, error: toastError } = useToast()

/**
 * Totale click social da array [{social,count}, ...]
 */
const socialTotal = (arr) => {
  if (!arr || !Array.isArray(arr)) return 0
  return arr.reduce((acc, s) => acc + (s.count || 0), 0)
}

const loadCards = async () => {
  loading.value = true
  try {
    // inizialmente solo lista card
    const raw = await $api('/cards')
    // aggiungo campo _stats che popoleremo dopo
    cards.value = raw.map((c) => ({
      ...c,
      _stats: null
    }))

    // carico le statistiche per ogni card (in parallelo)
    await Promise.all(
      cards.value.map(async (c) => {
        try {
          const stats = await $api(`/analytics/cards/${c.id}/summary`)
          c._stats = stats
        } catch (err) {
          console.error('Errore stats card', c.id, err)
          c._stats = { views_7d: 0, total_vcard: 0, social_clicks: [] }
        }
      })
    )
  } finally {
    loading.value = false
  }
}

const confirmDelete = async (c) => {
  if (!confirm(`Eliminare “${c.title}”?`)) return

  try {
    await $api(`/cards/${c.id}`, { method: 'DELETE' })
    cards.value = cards.value.filter((x) => x.id !== c.id)

    /* 🟢 TOAST SUCCESSO ELIMINAZIONE */
    success('Card eliminata con successo.')
  } catch (e) {
    console.error(e)

    /* 🔴 TOAST ERRORE ELIMINAZIONE */
    toastError('Errore durante l’eliminazione della card.')
  }
}

onMounted(loadCards)
</script>
