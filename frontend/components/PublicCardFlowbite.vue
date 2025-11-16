<!-- components/PublicCardFlowbite.vue -->
<template>
  <section class="bg-white dark:bg-gray-900">
    <div class="flex items-center justify-center min-h-screen py-6">
      <div class="bg-white p-6 rounded-lg shadow-lg dark:bg-gray-900 border-solid border border-gray-200">
        <div class="w-full sm:w-[550px] p-4 bg-white sm:p-6 dark:bg-gray-800 mx-auto rounded-lg">
          <!-- HEADER / AVATAR / TITOLO -->
          <div class="flex flex-col items-center pb-3">
            <img
              v-if="card.avatar_url"
              class="w-40 h-40 mb-3 rounded-full shadow-lg object-cover"
              :src="card.avatar_url"
              :alt="card.title"
            />
            <img
              v-else
              class="w-40 h-40 mb-3 rounded-full shadow-lg"
              src="/assets/images/profile-picture-3.jpg"
              alt="Profile"
            />

            <h5 class="mb-4 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
              <span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">   {{ card.title }}</span>
           
            </h5>

            <!-- Ruolo / Azienda -->
            <span
              v-if="subtitle"
              class="bg-yellow-100 text-yellow-800 shadow text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-yellow-900 dark:text-yellow-300 mb-2"
            >
              {{ subtitle }}
            </span>

            <!-- INFO PRINCIPALI (email / telefono / sito) -->
            <div class="mt-2 space-y-1 text-sm text-gray-700 dark:text-gray-300 text-center">
              <div v-if="primary.email">
                📧
                <a :href="`mailto:${primary.email}`" class="underline hover:no-underline">
                  {{ primary.email }}
                </a>
              </div>
              <div v-if="primary.phone">
                📱
                <a :href="`tel:${primary.phone.replace(/\\s+/g, '')}`" class="underline hover:no-underline">
                  {{ primary.phone }}
                </a>
              </div>
              <div v-if="primary.website">
                🌐
                <a :href="primary.websiteHref" target="_blank" rel="noopener" class="underline hover:no-underline">
                  {{ primary.website }}
                </a>
              </div>
            </div>
          </div>

          <!-- BIO -->
        
<p class="mb-3 text-center text-body text-gray-400">

            {{ card.notes }}
          </p>

          <!-- vCard -->
          <div class="mt-4 flex items-center justify-center gap-3">
            <a
              v-if="showVcard"
              :href="vcardUrl"
              class="inline-flex items-center px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              💾 Scarica vCard
            </a>
          </div>

     <!-- SOLO SOCIAL NELLA LISTA -->
<PublicSocialList
  :card-title="card.title"
  :card-id="card.id"       
  :fields="visibleFields"
/>
          <!-- QR -->
          <div class="flex items-center justify-center">
            <img
              :src="qrUrl"
               :alt="`QR code dei contatti di ${card.title}`"
              class="w-40 h-40 rounded border border-gray-200 dark:border-gray-700"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>



<script setup>
import { computed } from 'vue'
import PublicSocialList from '~/components/PublicSocialList.vue'

const props = defineProps({
  card: { type: Object, required: true },
  vcardUrl: { type: String, required: true },
  qrUrl: { type: String, required: true },
  visibleFields: { type: Array, required: true }
})

/* --------------------------------
 *  UTILITY BASE
 * -------------------------------- */
const showVcard = computed(() => !!(props.card && props.card.allow_vcard === true))

function firstField(fields, types) {
  const t = (types || []).map(s => String(s).toLowerCase())
  return (fields || []).find(
    x => t.includes(String(x.type || '').toLowerCase()) && x.value
  )
}

function firstValue(fields, types) {
  const f = firstField(fields, types)
  return f ? String(f.value || '') : ''
}

function normalizeUrl(v) {
  const s = String(v || '').trim()
  if (!s) return ''
  return /^https?:\/\//i.test(s) ? s : `https://${s}`
}

/* --------------------------------
 *  SOTTOTITOLO E INFO PRINCIPALI
 * -------------------------------- */
const subtitle = computed(() => {
  const role = firstValue(props.visibleFields, ['role', 'title', 'job'])
  const company = firstValue(props.visibleFields, ['company', 'org', 'organization'])
  if (role && company) return `${role} – ${company}`
  return role || company || ''
})

const primary = computed(() => {
  const email = firstValue(props.visibleFields, ['email'])
  const phone = firstValue(props.visibleFields, ['mobile', 'phone', 'tel'])
  const websiteField = firstField(props.visibleFields, ['url', 'website', 'site', 'link'])
  const website = websiteField ? String(websiteField.value || '') : ''
  return {
    email,
    phone,
    website,
    websiteHref: website ? normalizeUrl(website) : ''
  }
})
</script>
