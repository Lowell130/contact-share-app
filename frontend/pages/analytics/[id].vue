<!-- pages/analytics/[id].vue -->
<template>
  <section class="max-w-5xl mx-auto py-8">
    <h1 class="text-2xl font-bold mb-2">Analytics card</h1>
    <p class="text-sm text-gray-500 mb-6">
      Andamento visite e download vCard negli ultimi 30 giorni.
    </p>

    <div
      v-if="error"
      class="p-3 border border-red-300 bg-red-50 text-red-700 rounded mb-4"
    >
      {{ error }}
    </div>

    <div v-else-if="!data">
      Caricamento…
    </div>

    <div v-else class="space-y-8">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <p class="text-xs text-gray-500">Visite totali</p>
          <p class="text-2xl font-semibold">{{ data.total_views }}</p>
          <p class="text-xs text-gray-400 mt-1">Tutti i periodi</p>
        </div>

        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <p class="text-xs text-gray-500">vCard scaricate</p>
          <p class="text-2xl font-semibold">{{ data.total_vcard }}</p>
          <p class="text-xs text-gray-400 mt-1">Da sempre</p>
        </div>

        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <p class="text-xs text-gray-500">Visite ultime 24h</p>
          <p class="text-2xl font-semibold">{{ data.views_24h }}</p>
          <p class="text-xs text-gray-400 mt-1">Ultime 24 ore</p>
        </div>

        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <p class="text-xs text-gray-500">Visite ultimi 7 giorni</p>
          <p class="text-2xl font-semibold">{{ data.views_7d }}</p>
          <p class="text-xs text-gray-400 mt-1">Rolling 7 giorni</p>
        </div>
      </div>

      <!-- Chart visite ultimi 30 giorni -->
      <div class="p-4 md:p-6 rounded-2xl bg-white border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-gray-700">
            Visite ultimi 30 giorni
          </h2>
          <span class="text-xs text-gray-400">
            Totale: {{ totalLast30d }}
          </span>
        </div>

        <div v-if="hasChartData" ref="chartEl" class="w-full h-64" />
        <p v-else class="text-sm text-gray-500">
          Nessuna visita registrata negli ultimi 30 giorni.
        </p>
      </div>

      <!-- Referrer, Device, Social (liste testuali) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Referrer -->
        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">Top referrer</h3>
          <ul v-if="data.top_referrers.length" class="divide-y text-sm">
            <li
              v-for="r in data.top_referrers"
              :key="r.ref"
              class="flex items-center justify-between py-2"
            >
              <span class="truncate max-w-[180px]" :title="r.ref">
                {{
                  r.ref === 'direct'
                    ? 'Digitazione diretta / Nessun referrer'
                    : r.ref
                }}
              </span>
              <span class="font-mono text-xs text-gray-600">
                {{ r.count }}
              </span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500">
            Ancora nessun referrer disponibile.
          </p>
        </div>

        <!-- Device (lista) -->
        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">Device</h3>
          <ul v-if="data.devices.length" class="divide-y text-sm">
            <li
              v-for="d in data.devices"
              :key="d.kind"
              class="flex items-center justify-between py-2"
            >
              <span class="capitalize">
                {{ labelDevice(d.kind) }}
              </span>
              <span class="font-mono text-xs text-gray-600">
                {{ d.count }}
              </span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500">
            Nessun dato device per il periodo considerato.
          </p>
        </div>

        <!-- Social (lista) -->
        <div class="p-4 rounded-xl bg-white border shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">
            Click sui social (ultimi 30 giorni)
          </h3>
          <ul
            v-if="data.social_clicks && data.social_clicks.length"
            class="divide-y text-sm"
          >
            <li
              v-for="s in data.social_clicks"
              :key="s.social"
              class="flex items-center justify-between py-2"
            >
              <span>{{ labelSocial(s.social) }}</span>
              <span class="font-mono text-xs text-gray-600">
                {{ s.count }}
              </span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500">
            Nessun click sui social nel periodo considerato.
          </p>
        </div>
      </div>

      <!-- Device / Social charts -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Donut Device -->
        <div class="p-4 md:p-6 rounded-2xl bg-white border border-gray-200 shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">
            Distribuzione device (ultimi 30 giorni)
          </h3>
          <div v-if="hasDeviceData" ref="deviceChartEl" class="w-full h-60" />
          <p v-else class="text-sm text-gray-500">
            Nessun dato device sufficiente per il grafico.
          </p>
        </div>

        <!-- Bar Social -->
        <div class="p-4 md:p-6 rounded-2xl bg-white border border-gray-200 shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">
            Click per social (ultimi 30 giorni)
          </h3>
          <div v-if="hasSocialData" ref="socialChartEl" class="w-full h-60" />
          <p v-else class="text-sm text-gray-500">
            Nessun click sui social sufficiente per il grafico.
          </p>
        </div>
      </div>

      <!-- 🌍 Geo analytics -->
      <div class="p-4 md:p-6 rounded-2xl bg-white border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-semibold text-gray-700">
            Provenienza visite (ultimi 30 giorni)
          </h3>
          <span
            v-if="data.top_countries && data.top_countries.length"
            class="text-xs text-gray-400"
          >
            Paesi: {{ data.top_countries.length }}
          </span>
        </div>
        <div v-if="hasGeoData" ref="geoChartEl" class="w-full h-72" />
        <p v-else class="text-sm text-gray-500">
          Nessun dato geografico disponibile per il periodo considerato.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
  watch,
  nextTick,
} from 'vue'

const route = useRoute()
const { $api } = useApi()

const data = ref(null)
const error = ref('')

/** Elementi DOM per i grafici */
const chartEl = ref(null)         // line chart visite
const deviceChartEl = ref(null)   // donut device
const socialChartEl = ref(null)   // bar social
const geoChartEl = ref(null)      // bar paesi

/** Istanze ApexCharts */
const chartInstance = ref(null)
const deviceChartInstance = ref(null)
const socialChartInstance = ref(null)
const geoChartInstance = ref(null)

/** Cache di ApexCharts */
let ApexChartsLib = null
const getApex = async () => {
  if (!process.client) return null
  if (ApexChartsLib) return ApexChartsLib
  const mod = await import('apexcharts')
  ApexChartsLib = mod.default
  return ApexChartsLib
}

/** Carica le analytics dal backend */
const fetchAnalytics = async () => {
  try {
    error.value = ''
    data.value = await $api(`/analytics/cards/${route.params.id}/summary`)
    if (process.client) {
      await nextTick()
      await initAllCharts()
    }
  } catch (e) {
    console.error(e)
    error.value = 'Impossibile caricare le analytics della card.'
  }
}

onMounted(fetchAnalytics)
watch(
  () => route.params.id,
  async () => {
    await fetchAnalytics()
  }
)

/** Somma delle visite negli ultimi 30 giorni */
const totalLast30d = computed(() => {
  if (!data.value) return 0
  return (data.value.last30d || []).reduce(
    (acc, p) => acc + (p.count || 0),
    0
  )
})

/** Flag presenza dati */
const hasChartData = computed(() => {
  return !!(data.value && data.value.last30d && data.value.last30d.length)
})

const hasDeviceData = computed(() => {
  return !!(data.value && data.value.devices && data.value.devices.length)
})

const hasSocialData = computed(() => {
  return !!(
    data.value &&
    data.value.social_clicks &&
    data.value.social_clicks.length
  )
})

const hasGeoData = computed(() => {
  return !!(
    data.value &&
    data.value.top_countries &&
    data.value.top_countries.length
  )
})

/** Colore brand (da CSS var, con fallback) */
const brandColor = computed(() => {
  if (process.client) {
    const cs = getComputedStyle(document.documentElement)
    const v = cs.getPropertyValue('--color-fg-brand').trim()
    if (v) return v
  }
  return '#0ea5e9' // fallback (sky-500)
})

/** Opzioni area chart visite */
const chartOptions = computed(() => {
  if (!data.value || !data.value.last30d) return null

  const categories = data.value.last30d.map((p) => p.date)
  const seriesData = data.value.last30d.map((p) => p.count)

  return {
    chart: {
      height: '100%',
      type: 'area',
      fontFamily:
        'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      toolbar: { show: false },
      dropShadow: { enabled: false },
      zoom: { enabled: false },
    },
    series: [
      {
        name: 'Visite',
        data: seriesData,
        color: brandColor.value,
      },
    ],
    dataLabels: { enabled: false },
    stroke: {
      width: 4,
      curve: 'smooth',
    },
    fill: {
      type: 'gradient',
      gradient: {
        opacityFrom: 0.55,
        opacityTo: 0,
        gradientToColors: [brandColor.value],
      },
    },
    grid: {
      borderColor: '#e5e7eb',
      strokeDashArray: 4,
      padding: { left: 8, right: 8, top: 0, bottom: 0 },
    },
    xaxis: {
      categories,
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
        rotate: -45,
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
        formatter: (val) => Math.round(val),
      },
      min: 0,
    },
    tooltip: {
      x: { show: true },
    },
  }
})

/** Donut device */
const deviceChartOptions = computed(() => {
  if (!hasDeviceData.value) return null
  const labels = data.value.devices.map((d) => labelDevice(d.kind))
  const series = data.value.devices.map((d) => d.count)
  return {
    chart: {
      type: 'donut',
      height: '100%',
      toolbar: { show: false },
    },
    labels,
    series,
    colors: ['#0ea5e9', '#22c55e', '#6366f1', '#f97316'],
    legend: {
      position: 'bottom',
      labels: { colors: '#4b5563' },
    },
    stroke: {
      width: 1,
      colors: ['#ffffff'],
    },
    dataLabels: { enabled: false },
  }
})

/** Bar social */
const socialChartOptions = computed(() => {
  if (!hasSocialData.value) return null
  const sorted = [...data.value.social_clicks].sort(
    (a, b) => b.count - a.count
  )
  const categories = sorted.map((s) => labelSocial(s.social))
  const seriesData = sorted.map((s) => s.count)

  return {
    chart: {
      type: 'bar',
      height: '100%',
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 4,
      },
    },
    series: [
      {
        name: 'Click',
        data: seriesData,
      },
    ],
    xaxis: {
      categories,
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
      },
    },
    yaxis: {
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
      },
    },
    colors: ['#0ea5e9'],
    dataLabels: { enabled: false },
    grid: {
      borderColor: '#e5e7eb',
      strokeDashArray: 4,
    },
  }
})

/** Bar paesi (geo) */
const geoChartOptions = computed(() => {
  if (!hasGeoData.value) return null
  const sorted = [...data.value.top_countries].sort(
    (a, b) => b.count - a.count
  )
  const categories = sorted.map((c) => c.country || 'unknown')
  const seriesData = sorted.map((c) => c.count)

  return {
    chart: {
      type: 'bar',
      height: '100%',
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        borderRadius: 4,
      },
    },
    series: [
      {
        name: 'Visite',
        data: seriesData,
      },
    ],
    xaxis: {
      categories,
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
      },
    },
    yaxis: {
      labels: {
        style: { colors: '#6b7280', fontSize: '11px' },
      },
      min: 0,
    },
    colors: ['#0ea5e9'],
    dataLabels: { enabled: false },
    grid: {
      borderColor: '#e5e7eb',
      strokeDashArray: 4,
    },
    tooltip: {
      x: { show: true },
    },
  }
})

/** Inizializza / aggiorna tutti i grafici */
const initAllCharts = async () => {
  if (!process.client) return
  const ApexCharts = await getApex()
  if (!ApexCharts) return

  // line/area visite
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
  if (chartEl.value && hasChartData.value && chartOptions.value) {
    chartInstance.value = new ApexCharts(chartEl.value, chartOptions.value)
    await chartInstance.value.render()
  }

  // donut device
  if (deviceChartInstance.value) {
    deviceChartInstance.value.destroy()
    deviceChartInstance.value = null
  }
  if (deviceChartEl.value && hasDeviceData.value && deviceChartOptions.value) {
    deviceChartInstance.value = new ApexCharts(
      deviceChartEl.value,
      deviceChartOptions.value
    )
    await deviceChartInstance.value.render()
  }

  // bar social
  if (socialChartInstance.value) {
    socialChartInstance.value.destroy()
    socialChartInstance.value = null
  }
  if (socialChartEl.value && hasSocialData.value && socialChartOptions.value) {
    socialChartInstance.value = new ApexCharts(
      socialChartEl.value,
      socialChartOptions.value
    )
    await socialChartInstance.value.render()
  }

  // bar geo (paesi)
  if (geoChartInstance.value) {
    geoChartInstance.value.destroy()
    geoChartInstance.value = null
  }
  if (geoChartEl.value && hasGeoData.value && geoChartOptions.value) {
    geoChartInstance.value = new ApexCharts(
      geoChartEl.value,
      geoChartOptions.value
    )
    await geoChartInstance.value.render()
  }
}

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
  if (deviceChartInstance.value) {
    deviceChartInstance.value.destroy()
    deviceChartInstance.value = null
  }
  if (socialChartInstance.value) {
    socialChartInstance.value.destroy()
    socialChartInstance.value = null
  }
  if (geoChartInstance.value) {
    geoChartInstance.value.destroy()
    geoChartInstance.value = null
  }
})

/** Label per device */
const labelDevice = (kind) => {
  if (kind === 'mobile') return 'Mobile'
  if (kind === 'desktop') return 'Desktop'
  if (kind === 'tablet') return 'Tablet'
  return 'Altro'
}

/** Label carine per i social */
const labelSocial = (t) => {
  const k = (t || '').toLowerCase()

  if (!k || k === 'unknown') {
    return 'Altro / non rilevato'
  }

  const map = {
    facebook: 'Facebook',
    instagram: 'Instagram',
    linkedin: 'LinkedIn',
    x: 'X / Twitter',
    twitter: 'X / Twitter',
    github: 'GitHub',
    youtube: 'YouTube',
    tiktok: 'TikTok',
    twitch: 'Twitch',
    strava: 'Strava',
    telegram: 'Telegram',
    whatsapp: 'WhatsApp',
    onlyfans: 'OnlyFans',
    dribbble: 'Dribbble',
  }

  return map[k] || k
}
</script>
