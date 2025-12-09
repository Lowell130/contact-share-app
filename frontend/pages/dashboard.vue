<!-- pages/dashboard.vue -->
<template>
  <section class="max-w-5xl mx-auto py-8">
    <!-- Header di Benvenuto -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-2">Welcome to your overview.</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Loading data...</p>
    </div>

    <div v-else class="space-y-8">
      <!-- Statistiche Globali -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Visite Totali -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-medium text-gray-500">Total Views (7d)</h3>
            <div class="p-2 bg-blue-50 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ totalStats.views }}</p>
        </div>

        <!-- Download vCard -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-medium text-gray-500">Download vCard</h3>
            <div class="p-2 bg-green-50 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ totalStats.vCards }}</p>
        </div>

        <!-- Click Social -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-medium text-gray-500">Click Social</h3>
            <div class="p-2 bg-purple-50 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </div>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ totalStats.social }}</p>
        </div>
      </div>

      <!-- Top Card & Azioni Rapide -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Top Card -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Top Performance</h2>
          <div v-if="topCard" class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-full bg-gray-100 overflow-hidden flex-shrink-0 border border-gray-200">
              <img 
                v-if="topCard.avatar_url" 
                :src="resolveAvatar(topCard.avatar_url)" 
                :alt="topCard.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-base font-medium text-gray-900 truncate">{{ topCard.title }}</h3>
              <p class="text-sm text-gray-500 truncate">/c/{{ topCard.slug }}</p>
              <div class="mt-2 flex items-center gap-4 text-sm">
                <span class="text-blue-600 font-medium">{{ topCard._stats?.views_7d || 0 }} views</span>
                <NuxtLink :to="`/analytics/${topCard.id}`" class="text-gray-500 hover:text-gray-700 underline">
                  View details
                </NuxtLink>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-500">
            No active cards with recent visits.
          </div>
        </div>

        <!-- Azioni Rapide -->
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-center">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div class="space-y-3">
            <NuxtLink 
              to="/cards/new" 
              class="block w-full py-3 px-4 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors"
            >
              + Create New Card
            </NuxtLink>
            <NuxtLink 
              to="/cards" 
              class="block w-full py-3 px-4 bg-white border border-gray-300 text-gray-700 text-center rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Manage your Cards
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const { $api } = useApi()
const config = useRuntimeConfig()
const loading = ref(true)
const cards = ref([])

const resolveAvatar = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${config.public.apiBase}${url}`
}

const totalStats = computed(() => {
  return cards.value.reduce((acc, card) => {
    const stats = card._stats || { views_7d: 0, total_vcard: 0, social_clicks: [] }
    const socialCount = Array.isArray(stats.social_clicks) 
      ? stats.social_clicks.reduce((sum, s) => sum + (s.count || 0), 0) 
      : 0
    
    return {
      views: acc.views + (stats.views_7d || 0),
      vCards: acc.vCards + (stats.total_vcard || 0),
      social: acc.social + socialCount
    }
  }, { views: 0, vCards: 0, social: 0 })
})

const topCard = computed(() => {
  if (!cards.value.length) return null
  // Ordina per visite decrescenti
  return [...cards.value].sort((a, b) => {
    const viewsA = a._stats?.views_7d || 0
    const viewsB = b._stats?.views_7d || 0
    return viewsB - viewsA
  })[0]
})

onMounted(async () => {
  try {
    loading.value = true
    const rawCards = await $api('/cards')
    
    // Fetch stats for all cards in parallel
    const cardsWithStats = await Promise.all(rawCards.map(async (c) => {
      try {
        const stats = await $api(`/analytics/cards/${c.id}/summary`)
        return { ...c, _stats: stats }
      } catch (e) {
        console.error(`Failed to load stats for card ${c.id}`, e)
        return { ...c, _stats: { views_7d: 0, total_vcard: 0, social_clicks: [] } }
      }
    }))
    
    cards.value = cardsWithStats
  } catch (e) {
    console.error('Failed to load dashboard data', e)
  } finally {
    loading.value = false
  }
})
</script>
