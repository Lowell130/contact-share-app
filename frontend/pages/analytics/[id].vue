<!-- pages/analytics/[id].vue -->
<template>
  <section class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-heading">Analytics Dashboard</h1>
      <p class="text-body mt-2">
Track your card’s performance and user engagement.
      </p>
    </div>

    <!-- ERROR -->
    <div
      v-if="error"
      class="p-4 mb-6 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
      role="alert"
    >
      <span class="font-medium">Error!</span> {{ error }}
    </div>

    <div v-else-if="!data" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else class="space-y-6">
      <!-- KPI Cards (Always visible for all users) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- KPI 1 -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm font-medium text-body">Total Views</p>
              <h3 class="text-2xl font-bold text-heading mt-2">{{ data.total_views }}</h3>
            </div>
            <div class="p-2 bg-blue-50 rounded-lg dark:bg-blue-900/20">
              <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-green-500 flex items-center font-medium">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
              +{{ data.views_24h }}
            </span>
            <span class="text-body ml-2">nelle ultime 24h</span>
          </div>
        </div>

        <!-- KPI 2 -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm font-medium text-body">vCard Downloads</p>
              <h3 class="text-2xl font-bold text-heading mt-2">{{ data.total_vcard }}</h3>
            </div>
            <div class="p-2 bg-purple-50 rounded-lg dark:bg-purple-900/20">
              <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-body">Conversion rate: </span>
            <span class="font-medium text-heading ml-1">{{ conversionRate }}%</span>
          </div>
        </div>

        <!-- KPI 3 -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm font-medium text-body">Views (7d)</p>
              <h3 class="text-2xl font-bold text-heading mt-2">{{ data.views_7d }}</h3>
            </div>
            <div class="p-2 bg-green-50 rounded-lg dark:bg-green-900/20">
              <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-body">Weekly trend</span>
          </div>
        </div>

        <!-- KPI 4 -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm font-medium text-body">Unique Countries</p>
              <h3 class="text-2xl font-bold text-heading mt-2">{{ data.top_countries.length }}</h3>
            </div>
            <div class="p-2 bg-orange-50 rounded-lg dark:bg-orange-900/20">
              <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm">
            <span class="text-body">Global reach</span>
          </div>
        </div>
      </div>

      <!-- 🆕 UPGRADE BOX FOR FREE USERS -->
      <div v-if="!isPro" class="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-lg p-8 text-center">
        <div class="max-w-2xl mx-auto">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Unlock Advanced Analytics</h3>
          <p class="text-gray-600 mb-6">
            Upgrade to PRO to access detailed charts, device analysis, geographic data, referrers, and social clicks.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-3 justify-center items-center mb-4">
            <div class="flex items-center text-sm text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              Interactive charts
            </div>
            <div class="flex items-center text-sm text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              Device analysis
            </div>
            <div class="flex items-center text-sm text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              Geographic data
            </div>
          </div>
          
          <NuxtLink 
            to="/upgrade"
            class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
          >
            Upgrade to PRO - €4.99/month
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
          </NuxtLink>
        </div>
      </div>

      <!-- 🔒 ADVANCED ANALYTICS (PRO ONLY) -->
      <template v-if="isPro">
        <!-- MAIN CHART (User Template) -->
        <div class="w-full bg-neutral-primary-soft border border-default rounded-base shadow-xs p-4 md:p-6">
          <div class="flex justify-between items-start">
            <div>
              <h5 class="text-2xl font-semibold text-heading">{{ totalLast30d }}</h5>
              <p class="text-body">Views last {{ selectedDays }} days</p>
            </div>
            <div class="flex items-center px-2.5 py-0.5 font-medium text-fg-success text-center bg-success-soft rounded-full">
              <svg class="w-5 h-5 mr-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v13m0-13 4 4m-4-4-4 4"/></svg>
              Active
            </div>
          </div>
          
          <!-- Chart Container -->
          <div ref="chartEl" class=""></div>
          
          <div class="grid grid-cols-1 items-center border-light border-t justify-between mt-4">
            <div class="flex justify-between items-center pt-4 md:pt-6">
              <!-- Button -->
              <div class="relative">
                <button @click="isDropdownOpen = !isDropdownOpen" class="text-sm font-medium text-body hover:text-heading text-center inline-flex items-center" type="button">
                    Last {{ selectedDays }} days
                    <svg class="w-4 h-4 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/></svg>
                </button>
                <!-- Dropdown menu -->
                <div v-if="isDropdownOpen" class="absolute z-10 bg-neutral-primary-medium border border-default-medium rounded-base shadow-lg w-44 mt-2">
                    <ul class="p-2 text-sm text-body font-medium">
                      <li><a href="#" @click.prevent="setDays(7); isDropdownOpen=false" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Last 7 days</a></li>
                      <li><a href="#" @click.prevent="setDays(30); isDropdownOpen=false" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Last 30 days</a></li>
                      <li><a href="#" @click.prevent="setDays(90); isDropdownOpen=false" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Last 90 days</a></li>
                    </ul>
                </div>
              </div>
              <a href="#" @click.prevent="exportCsv" class="inline-flex items-center text-fg-brand bg-transparent box-border border border-transparent hover:bg-neutral-secondary-medium focus:ring-4 focus:ring-neutral-tertiary font-medium leading-5 rounded-base text-sm px-3 py-2 focus:outline-none">
                Full Report (CSV)
                <svg class="w-4 h-4 ms-1.5 -me-0.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4"/></svg>
              </a>
            </div>
          </div>
        </div>

      <!-- SECONDARY GRIDS -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- DEVICE CHART -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <h3 class="text-lg font-bold text-heading mb-4">Devices</h3>
          <div v-if="hasDeviceData" ref="deviceChartEl" class="h-64"></div>
          <div v-else class="h-64 flex items-center justify-center text-body text-sm">Insufficient data</div>
        </div>

        <!-- OS CHART -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
          <h3 class="text-lg font-bold text-heading mb-4">Operating Systems</h3>
          <div v-if="hasOsData" ref="osChartEl" class="h-64"></div>
          <div v-else class="h-64 flex items-center justify-center text-body text-sm">Insufficient data</div>
        </div>

        <!-- GEO CHART -->
        <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6 lg:col-span-2">
          <h3 class="text-lg font-bold text-heading mb-4">Geographic Origin</h3>
          <div v-if="hasGeoData" ref="geoChartEl"></div>
          <div v-else class="flex items-center justify-center text-body text-sm">Insufficient data</div>
        </div>
      </div>

      <!-- SOCIAL CLICKS (New Template) -->
      <div class="w-full bg-neutral-primary-soft border border-default rounded-base shadow-xs p-4 md:p-6">
        <div class="flex justify-between border-light border-b pb-3 mb-3">
          <dl>
            <dt class="text-body">Social Clicks</dt>
            <dd class="text-2xl font-semibold text-heading">{{ totalSocialClicks }}</dd>
          </dl>
          <div>
            <span class="inline-flex items-center bg-success-soft border border-success-subtle text-fg-success-strong text-xs font-medium px-1.5 py-0.5 rounded">
              <svg class="w-4 h-4 me-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v13m0-13 4 4m-4-4-4 4"/></svg>
              Engagement
            </span>
          </div>
        </div>
        
        <p class="text-sm text-body mb-4">
          Clicks on social and personal links in your card.
        </p>

        <div v-if="hasSocialData" class="space-y-4">
          <div v-for="s in data.social_clicks" :key="s.social" class="relative">
            <div class="flex items-center justify-between mb-1 relative z-10">
              <div class="flex items-center space-x-3">
                <div class="text-body p-1.5 bg-gray-50 dark:bg-gray-700/50 rounded-lg" v-html="getReferrerIcon(s.social)"></div>
                <span class="font-medium text-heading text-sm">
                  {{ labelSocial(s.social) }}
                </span>
              </div>
              <div class="text-right">
                <span class="block font-bold text-heading text-sm">{{ s.count }}</span>
                <span class="text-xs text-body">{{ getSocialPercentage(s.count) }}%</span>
              </div>
            </div>
            <!-- Progress Bar Background -->
            <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5 overflow-hidden">
              <div class="bg-purple-500 h-1.5 rounded-full" :style="{ width: getSocialPercentage(s.count) + '%' }"></div>
            </div>
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-8 text-center">
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-full mb-3">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
          </div>
          <p class="text-body text-sm">No social clicks yet</p>
        </div>
          
        <div class="grid grid-cols-1 items-center border-light border-t justify-between mt-4">
          <div class="flex justify-between items-center pt-4 md:pt-6">
            <!-- Button -->
            <div class="relative">
              <button @click="isSocialDropdownOpen = !isSocialDropdownOpen" class="text-sm font-medium text-body hover:text-heading text-center inline-flex items-center" type="button">
                  Last 30 days
                  <svg class="w-4 h-4 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/></svg>
              </button>
              <!-- Dropdown menu -->
              <div v-if="isSocialDropdownOpen" class="absolute z-10 bottom-full mb-2 bg-neutral-primary-medium border border-default-medium rounded-base shadow-lg w-44">
                  <ul class="p-2 text-sm text-body font-medium">
                    <li><a href="#" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Last 7 days</a></li>
                    <li><a href="#" class="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded">Last 30 days</a></li>
                  </ul>
              </div>
            </div>
            <a href="#" class="inline-flex items-center text-fg-brand bg-transparent box-border border border-transparent hover:bg-neutral-secondary-medium focus:ring-4 focus:ring-neutral-tertiary font-medium leading-5 rounded-base text-sm px-3 py-2 focus:outline-none">
              Social Report
              <svg class="w-4 h-4 ms-1.5 -me-0.5 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4"/></svg>
            </a>
          </div>
        </div>
      </div>

      <!-- REFERRERS LIST -->
      <div class="bg-neutral-primary-soft border border-default rounded-base shadow-xs p-6">
        <h3 class="text-lg font-bold text-heading mb-4">Top Referrers</h3>
        
        <div v-if="data.top_referrers && data.top_referrers.length" class="space-y-4">
          <div v-for="r in data.top_referrers" :key="r.ref" class="relative">
            <div class="flex items-center justify-between mb-1 relative z-10">
              <div class="flex items-center space-x-3">
                <div class="text-body p-1.5 bg-gray-50 dark:bg-gray-700/50 rounded-lg" v-html="getReferrerIcon(r.ref)"></div>
                <span class="font-medium text-heading text-sm">
                  {{ r.ref === 'direct' ? 'Direct / No referrer' : r.ref }}
                </span>
              </div>
              <div class="text-right">
                <span class="block font-bold text-heading text-sm">{{ r.count }}</span>
                <span class="text-xs text-body">{{ getReferrerPercentage(r.count) }}%</span>
              </div>
            </div>
            <!-- Progress Bar Background -->
            <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5 overflow-hidden">
              <div class="bg-blue-500 h-1.5 rounded-full" :style="{ width: getReferrerPercentage(r.count) + '%' }"></div>
            </div>
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-8 text-center">
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-full mb-3">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
          </div>
          <p class="text-body text-sm">No referrer data available</p>
        </div>
      </div>

    </template>
    <!-- End PRO-only sections -->

    </div>

    
  </section>
</template>



<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

const route = useRoute()
const { $api } = useApi()
const { user, accessToken } = useAuth()

// Check if user is PRO
const isPro = computed(() => user.value?.plan === 'pro' || user.value?.plan === 'admin')

const data = ref(null)
const error = ref('')
const selectedDays = ref(30)
const isDropdownOpen = ref(false)
const isSocialDropdownOpen = ref(false)

// Chart Elements
const chartEl = ref(null)
const deviceChartEl = ref(null)
const socialChartEl = ref(null)
const geoChartEl = ref(null)
const osChartEl = ref(null)

// Chart Instances
let chartInstance = null
let deviceChartInstance = null
let socialChartInstance = null
let geoChartInstance = null
let osChartInstance = null

// Load ApexCharts dynamically
let ApexChartsLib = null
const getApex = async () => {
  if (!process.client) return null
  if (ApexChartsLib) return ApexChartsLib
  const mod = await import('apexcharts')
  ApexChartsLib = mod.default
  return ApexChartsLib
}

const fetchAnalytics = async () => {
  try {
    error.value = ''
    data.value = await $api(`/analytics/cards/${route.params.id}/summary?days=${selectedDays.value}`)
    if (process.client) {
      await nextTick()
      await initAllCharts()
    }
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile caricare le analytics.'
  }
}

const setDays = (d) => {
    selectedDays.value = d
    fetchAnalytics()
}

const exportCsv = async () => {
    if (!isPro.value) return
    try {
        const token = accessToken.value 
        const res = await fetch(`${useRuntimeConfig().public.apiBase}/analytics/cards/${route.params.id}/export?days=${selectedDays.value}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) throw new Error("Export failed")
        
        const blob = await res.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `analytics_${route.params.id}_${selectedDays.value}d.csv`
        document.body.appendChild(a)
        a.click()
        a.remove()
    } catch(e) {
        console.error("CSV Export error", e)
        alert("Export failed")
    }
}

onMounted(fetchAnalytics)
watch(() => route.params.id, fetchAnalytics)

// Computed Helpers
const totalLast30d = computed(() => data.value?.last30d?.reduce((acc, p) => acc + (p.count || 0), 0) || 0)
const conversionRate = computed(() => {
  if (!data.value || !data.value.total_views) return 0
  return ((data.value.total_vcard / data.value.total_views) * 100).toFixed(1)
})

const hasDeviceData = computed(() => !!data.value?.devices?.length)
const hasSocialData = computed(() => !!data.value?.social_clicks?.length)
const hasGeoData = computed(() => !!data.value?.top_countries?.length)

const topSocialName = computed(() => {
  if (!hasSocialData.value) return '-'
  return labelSocial(data.value.social_clicks[0].social)
})
const topSocialCount = computed(() => {
  if (!hasSocialData.value) return 0
  return data.value.social_clicks[0].count
})

const totalDevice = computed(() => {
  if (!data.value || !data.value.devices) return 0
  return data.value.devices.reduce((acc, d) => acc + (d.count || 0), 0)
})

const totalSocialClicks = computed(() => {
  if (!data.value || !data.value.social_clicks) return 0
  return data.value.social_clicks.reduce((acc, s) => acc + (s.count || 0), 0)
})

// Referrers Helpers
const maxReferrerCount = computed(() => {
  if (!data.value?.top_referrers?.length) return 0
  return Math.max(...data.value.top_referrers.map(r => r.count))
})

const getReferrerPercentage = (count) => {
  if (!maxReferrerCount.value) return 0
  return Math.round((count / maxReferrerCount.value) * 100)
}

// Social Helpers
const maxSocialCount = computed(() => {
  if (!data.value?.social_clicks?.length) return 0
  return Math.max(...data.value.social_clicks.map(s => s.count))
})

const getSocialPercentage = (count) => {
  if (!maxSocialCount.value) return 0
  return Math.round((count / maxSocialCount.value) * 100)
}

const getReferrerIcon = (refName) => {
  const name = (refName || '').toLowerCase()
  
  // Direct
  if (name === 'direct' || name.includes('direct')) {
    return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>`
  }
  
  // Socials & Tech
  if (name.includes('google')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/></svg>`
  if (name.includes('facebook') || name.includes('fb')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>`
  if (name.includes('linkedin')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>`
  if (name.includes('instagram')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.069-4.85.069-3.204 0-3.584-.012-4.849-.069-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>`
  if (name.includes('twitter') || name.includes('t.co') || name.includes('x')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>`
  if (name.includes('github')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>`
  if (name.includes('youtube')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`
  if (name.includes('tiktok')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93v6.16c0 2.52-1.12 4.84-2.9 6.24-1.72 1.36-3.92 1.96-6.13 1.67-2.15-.29-4.13-1.42-5.49-3.1-1.36-1.68-1.9-3.85-1.5-5.96.38-2.06 1.61-3.9 3.4-4.97 1.76-1.05 3.87-1.19 5.76-.38.55.24 1.05.59 1.49 1.01v-4.2c-1.3-.22-2.64-.22-3.94.01-2.2.38-4.14 1.79-5.16 3.78-1.02 1.99-1.02 4.36 0 6.35 1.02 1.99 2.96 3.4 5.16 3.78 2.2.38 4.38-.38 5.88-2.04 1.5-1.66 2.06-3.96 1.5-6.16-.24-.94-.7-1.82-1.35-2.57-1.07-1.22-2.68-1.81-4.28-1.58v-4.03c1.6.23 3.21.82 4.28 2.04.65.75 1.11 1.63 1.35 2.57.56 2.2.01 4.5-1.5 6.16-1.5 1.66-3.68 2.42-5.88 2.04-2.2-.38-4.14-1.79-5.16-3.78-1.02-1.99-1.02-4.36 0-6.35 1.02-1.99 2.96-3.4 5.16 3.78 1.3.23 2.64.23 3.94.01v4.2c-.44-.42-.94-.77-1.49-1.01-1.89-.81-4-.67-5.76.38-1.79 1.07-3.02 2.91-3.4 4.97-.4 2.11.14 4.28 1.5 5.96 1.36 1.68 3.34 2.81 5.49 3.1 2.21.29 4.41-.31 6.13-1.67 1.78-1.4 2.9-3.72 2.9-6.24v-6.16c.52.34 1.05.67 1.62.93 1.31.62 2.76.92 4.2.97v-4.03c-1.54-.17-3.12-.68-4.24-1.79-1.12-1.08-1.67-2.64-1.75-4.17-1.3.01-2.6.0-3.91.02z"/></svg>`
  if (name.includes('twitch')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z"/></svg>`
  if (name.includes('whatsapp')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>`
  if (name.includes('telegram')) return `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 11.944 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>`
  
  // Default Globe
  return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>`
}

const brandColor = '#3b82f6' // Blue-500

// Chart Options
const chartOptions = computed(() => {
  if (!data.value?.last30d) return null
  return {
    chart: { height: '100%', type: 'area', fontFamily: 'Inter, sans-serif', toolbar: { show: false }, zoom: { enabled: false } },
    series: [{ name: 'Visite', data: data.value.last30d.map(p => p.count) }],
    colors: [brandColor],
    fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.05, stops: [0, 90, 100] } },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 3 },
    xaxis: { categories: data.value.last30d.map(p => p.date), labels: { show: false }, axisBorder: { show: false }, axisTicks: { show: false } },
    yaxis: { show: false },
    grid: { show: false, padding: { left: 0, right: 0, top: 0, bottom: 20 } }, // Added bottom padding
    tooltip: { x: { show: true } }
  }
})

const deviceChartOptions = computed(() => {
  if (!hasDeviceData.value) return null
  return {
    chart: { type: 'donut', height: '100%' },
    labels: data.value.devices.map(d => d.kind),
    series: data.value.devices.map(d => d.count),
    colors: ['#3b82f6', '#10b981', '#f59e0b', '#6366f1'],
    legend: { position: 'bottom' },
    dataLabels: { enabled: false }
  }
})

const hasOsData = computed(() => !!data.value?.os_breakdown?.length)
const osChartOptions = computed(() => {
  if (!hasOsData.value) return null
  return {
    chart: { type: 'pie', height: '100%' },
    labels: data.value.os_breakdown.map(o => o.os),
    series: data.value.os_breakdown.map(o => o.count),
    colors: ['#8b5cf6', '#ec4899', '#06b6d4', '#84cc16', '#64748b'],
    legend: { position: 'bottom' },
    dataLabels: { enabled: false }
  }
})

const socialChartOptions = computed(() => {
  if (!hasSocialData.value) return null
  return {
    chart: { type: 'bar', height: '100%', toolbar: { show: false } },
    plotOptions: { bar: { borderRadius: 4, horizontal: false, columnWidth: '50%' } }, // Changed to vertical bars
    series: [{ name: 'Click', data: data.value.social_clicks.map(s => s.count) }],
    xaxis: { 
      categories: data.value.social_clicks.map(s => labelSocial(s.social)),
      labels: { style: { colors: '#6b7280', fontSize: '11px' } }
    },
    yaxis: { show: false },
    colors: ['#8b5cf6'],
    grid: { borderColor: '#f3f4f6', strokeDashArray: 4 },
    dataLabels: { enabled: false }
  }
})

const geoChartOptions = computed(() => {
  if (!hasGeoData.value) return null
  return {
    chart: { type: 'bar', height: '100%', toolbar: { show: false } },
    plotOptions: { bar: { borderRadius: 4, columnWidth: '60%' } },
    series: [{ name: 'Visite', data: data.value.top_countries.map(c => c.count) }],
    xaxis: { categories: data.value.top_countries.map(c => c.country) },
    colors: ['#f97316'],
    grid: { borderColor: '#f3f4f6' }
  }
})

// Init Charts
const initAllCharts = async () => {
  if (!process.client) return
  const ApexCharts = await getApex()
  if (!ApexCharts) return

  // Destroy old instances
  if (chartInstance) chartInstance.destroy()
  if (deviceChartInstance) deviceChartInstance.destroy()
  if (socialChartInstance) socialChartInstance.destroy()
  if (geoChartInstance) geoChartInstance.destroy()
  if (osChartInstance) osChartInstance.destroy()

  if (chartEl.value && chartOptions.value) {
    chartInstance = new ApexCharts(chartEl.value, chartOptions.value)
    chartInstance.render()
  }
  if (deviceChartEl.value && deviceChartOptions.value) {
    deviceChartInstance = new ApexCharts(deviceChartEl.value, deviceChartOptions.value)
    deviceChartInstance.render()
  }
  if (osChartEl.value && osChartOptions.value) {
    osChartInstance = new ApexCharts(osChartEl.value, osChartOptions.value)
    osChartInstance.render()
  }
  if (socialChartEl.value && socialChartOptions.value) {
    socialChartInstance = new ApexCharts(socialChartEl.value, socialChartOptions.value)
    socialChartInstance.render()
  }
  if (geoChartEl.value && geoChartOptions.value) {
    geoChartInstance = new ApexCharts(geoChartEl.value, geoChartOptions.value)
    geoChartInstance.render()
  }
}

onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
  if (deviceChartInstance) deviceChartInstance.destroy()
  if (osChartInstance) osChartInstance.destroy()
  if (socialChartInstance) socialChartInstance.destroy()
  if (geoChartInstance) geoChartInstance.destroy()
})

const labelDevice = (kind) => {
  if (kind === 'mobile') return 'Mobile'
  if (kind === 'desktop') return 'Desktop'
  if (kind === 'tablet') return 'Tablet'
  return 'Other'
}

const labelSocial = (t) => {
  const k = (t || '').toLowerCase()
  if (!k || k === 'unknown') return 'Other'
  const map = {
    facebook: 'Facebook', instagram: 'Instagram', linkedin: 'LinkedIn',
    x: 'X', twitter: 'X', github: 'GitHub', youtube: 'YouTube',
    tiktok: 'TikTok', twitch: 'Twitch', strava: 'Strava',
    telegram: 'Telegram', whatsapp: 'WhatsApp', onlyfans: 'OnlyFans'
  }
  return map[k] || k
}
</script>
