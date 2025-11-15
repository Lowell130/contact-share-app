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

      <!-- Chart -->
      <div class="p-4 md:p-6 rounded-2xl bg-white border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between mb-3 ">
          <h2 class="text-sm font-semibold text-gray-700">
            Visite ultimi 30 giorni
          </h2>
          <span class="text-xs text-gray-400 ">
            Totale: {{ totalLast30d }}
          </span>
        </div>

        <!-- contenitore ApexCharts -->
        <div
          v-if="hasChartData"
          ref="chartEl"
          class="w-full h-64"
        />
        <p v-else class="text-sm text-gray-500">
          Nessuna visita registrata negli ultimi 30 giorni.
        </p>
      </div>

      <!-- Referrer & Device -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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

        <!-- Device -->
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

const chartEl = ref(null)
const chartInstance = ref(null)

/** Carica le analytics dal backend */
const fetchAnalytics = async () => {
  try {
    error.value = ''
    data.value = await $api(`/analytics/cards/${route.params.id}/summary`)
    // dopo aver caricato i dati, inizializza/aggiorna il grafico
    if (process.client) {
      await nextTick()
      await initChart()
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

/** Abbiamo dati per il grafico? */
const hasChartData = computed(() => {
  return !!(data.value && data.value.last30d && data.value.last30d.length)
})

/** Colore brand (da CSS var, con fallback) */
const brandColor = computed(() => {
  if (process.client) {
    const cs = getComputedStyle(document.documentElement)
    const v = cs.getPropertyValue('--color-fg-brand').trim()
    if (v) return v
  }
  return '#0ea5e9' // fallback (tipo sky-500)
})

/** Opzioni complete ApexCharts (area + gradiente) */
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

/** Inizializza / re-renderizza il grafico ApexCharts */
const initChart = async () => {
  if (!process.client) return
  if (!chartEl.value) return
  if (!hasChartData.value) {
    // se non ci sono dati, distruggi eventuale chart esistente
    if (chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
    return
  }

  const options = chartOptions.value
  if (!options) return

  const mod = await import('apexcharts')
  const ApexCharts = mod.default

  // distruggi l'istanza precedente se presente
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }

  chartInstance.value = new ApexCharts(chartEl.value, options)
  await chartInstance.value.render()
}

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
})

/** Label carine per i device */
const labelDevice = (kind) => {
  if (kind === 'mobile') return 'Mobile'
  if (kind === 'desktop') return 'Desktop'
  if (kind === 'tablet') return 'Tablet'
  return 'Altro'
}
</script>
