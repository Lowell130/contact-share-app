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
          class="shadow-sm px-3 py-3 flex justify-between items-center rounded-base border border-default bg-white hover:bg-neutral-secondary-soft/70 transition"
        >
          <!-- SINISTRA: avatar + info -->
          <div class="flex items-center gap-3 min-w-0">
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
            <div class="min-w-0">
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
          <div class="flex flex-wrap gap-2 justify-end ml-4">
            <NuxtLink
              :to="`/cards/${c.id}`"
              type="button"
              class="text-white bg-success box-border border border-transparent hover:bg-success-strong focus:ring-4 focus:ring-success-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
            >
              Modifica
            </NuxtLink>

            <a
              type="button"
              :href="`/c/${c.slug}`"
              target="_blank"
              class="text-body bg-neutral-secondary-medium box-border border border-default-medium hover:bg-neutral-tertiary-medium hover:text-heading focus:ring-4 focus:ring-neutral-tertiary shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
            >
              Apri pubblico
            </a>

            <button
              @click="confirmDelete(c)"
              class="text-white bg-danger box-border border border-transparent hover:bg-danger-strong focus:ring-4 focus:ring-danger-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
            >
              Elimina
            </button>

            <NuxtLink
              :to="`/analytics/${c.id}`"
              type="button"
              class="text-white bg-brand box-border border border-transparent hover:bg-brand-strong focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none"
            >
              Statistiche
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
