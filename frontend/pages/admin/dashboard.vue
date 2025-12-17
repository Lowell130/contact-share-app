<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- KPI Card: Users -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Total Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.users }}</p>
          </div>
          <div class="p-3 bg-blue-50 rounded-full text-blue-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          </div>
        </div>
      </div>

      <!-- KPI Card: Cards -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Total Cards</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.cards }}</p>
          </div>
          <div class="p-3 bg-indigo-50 rounded-full text-indigo-600">
             <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
          </div>
        </div>
      </div>

       <!-- KPI Card: Pro Users -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Pro Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.pro_users }}</p>
          </div>
          <div class="p-3 bg-amber-50 rounded-full text-amber-600">
             <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Users Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- New Users -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 font-semibold text-gray-800">
                Recent Signups
            </div>
            <div class="divide-y divide-gray-100">
                <div v-for="u in stats.recent_users" :key="u.email" class="px-6 py-3 flex items-center justify-between">
                    <div>
                        <div class="font-medium text-gray-800">{{ u.name || 'No Name' }}</div>
                        <div class="text-xs text-gray-500">{{ u.email }}</div>
                    </div>
                    <div class="text-xs text-gray-400">
                        {{ new Date(u.created_at).toLocaleDateString() }}
                    </div>
                </div>
                <div v-if="!stats.recent_users?.length" class="px-6 py-4 text-center text-gray-400 font-bold">
                    No users yet
                </div>
            </div>
        </div>

        <!-- Recent PRO -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 font-semibold text-gray-800 flex items-center gap-2">
                <span>Recent PRO Upgrades</span>
                <span class="px-2 py-0.5 rounded text-xs bg-amber-100 text-amber-700 font-bold">PRO</span>
            </div>
             <div class="divide-y divide-gray-100">
                <div v-for="u in stats.recent_pro_users" :key="u.email" class="px-6 py-3 flex items-center justify-between">
                    <div>
                        <div class="font-medium text-gray-800">{{ u.name || 'No Name' }}</div>
                        <div class="text-xs text-gray-500">{{ u.email }}</div>
                    </div>
                     <div class="text-xs text-gray-400">
                        {{ new Date(u.created_at).toLocaleDateString() }}
                    </div>
                </div>
                 <div v-if="!stats.recent_pro_users?.length" class="px-6 py-4 text-center text-gray-400 font-bold">
                    No PRO users yet
                </div>
            </div>
        </div>
    </div>

    <!-- Analytics Section -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-4">Global Analytics (Last 30 Days)</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Top Countries -->
            <div>
                <h4 class="text-sm font-semibold text-gray-600 mb-3 uppercase tracking-wide">Top Users Origins</h4>
                <div v-if="analytics.top_countries?.length" class="space-y-3">
                    <div v-for="item in analytics.top_countries" :key="item.country" class="relative">
                        <div class="flex justify-between text-sm mb-1">
                            <span class="font-medium text-gray-700 flex items-center gap-2">
                                {{ getFlagEmoji(item.country) }} {{ item.country }}
                            </span>
                            <span class="text-gray-500">{{ item.count }}</span>
                        </div>
                        <div class="w-full bg-gray-100 rounded-full h-2">
                            <div 
                                class="bg-blue-500 h-2 rounded-full transition-all duration-500"
                                :style="{ width: `${(item.count / maxCountryCount) * 100}%` }"
                            ></div>
                        </div>
                    </div>
                </div>
                 <div v-else class="text-gray-400 italic text-sm">No data available</div>
            </div>

            <!-- Top Referrers -->
            <div>
                 <h4 class="text-sm font-semibold text-gray-600 mb-3 uppercase tracking-wide">Top Referrers</h4>
                 <div v-if="analytics.top_referrers?.length" class="space-y-3">
                    <div v-for="item in analytics.top_referrers" :key="item.ref" class="relative">
                        <div class="flex justify-between text-sm mb-1">
                            <span class="font-medium text-gray-700 truncate max-w-[200px]" :title="item.ref">
                                {{ item.ref }}
                            </span>
                            <span class="text-gray-500">{{ item.count }}</span>
                        </div>
                        <div class="w-full bg-gray-100 rounded-full h-2">
                            <div 
                                class="bg-indigo-500 h-2 rounded-full transition-all duration-500"
                                :style="{ width: `${(item.count / maxRefCount) * 100}%` }"
                            ></div>
                        </div>
                    </div>
                </div>
                <div v-else class="text-gray-400 italic text-sm">No data available</div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
definePageMeta({ layout: 'admin', middleware: 'admin' })
const { $api } = useApi()

const stats = ref({ users: 0, cards: 0, pro_users: 0, recent_users: [], recent_pro_users: [] })
const analytics = ref({ top_countries: [], top_referrers: [], last30d: [] })

const maxCountryCount = computed(() => {
    if (!analytics.value.top_countries?.length) return 1
    return Math.max(...analytics.value.top_countries.map(c => c.count))
})

const maxRefCount = computed(() => {
     if (!analytics.value.top_referrers?.length) return 1
    return Math.max(...analytics.value.top_referrers.map(c => c.count))
})

// Simple flag helper
const getFlagEmoji = (countryCode) => {
  if (!countryCode || countryCode === 'unknown') return '🌍'
  const codePoints = countryCode
    .toUpperCase()
    .split('')
    .map(char =>  127397 + char.charCodeAt(0));
  return String.fromCodePoint(...codePoints);
}

onMounted(async () => {
    try {
        stats.value = await $api('/admin/stats')
        analytics.value = await $api('/admin/analytics/global')
    } catch(e) {
        console.error("Stats error", e)
    }
})
</script>
