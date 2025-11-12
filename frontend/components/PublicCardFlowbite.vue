<template>
  <section class="bg-white dark:bg-gray-900">
    <div class="flex items-center justify-center min-h-screen py-6">
      <div class="bg-white p-6 rounded-lg shadow-lg border-amber-500 border">
        <div class="w-full sm:w-[500px] p-4 bg-white sm:p-6 dark:bg-gray-800 mx-auto">
          <div class="flex flex-col items-center pb-3">
            <img class="w-40 h-40 mb-3 rounded-full shadow-lg" src="/assets/images/profile-picture-3.jpg" alt="Bonnie image"/>
            <h5 class="mb-4 text-3xl font-semibold text-gray-900 dark:text-white">{{card.title}}</h5>
            <span v-if="subtitle" class="bg-yellow-100 text-yellow-800 shadow text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-yellow-900 dark:text-yellow-300 mb-2">{{ subtitle }}</span>

       <!-- <div class="flex mt-4 md:mt-6">
             <a href="#" class="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add friend</a>
            <a href="#" class="py-2 px-4 ms-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">Message</a>
      
        </div> -->
    </div>
         
 <div class="mb-6 border border-cyan-700 p-4 rounded-lg bg-amber-600">
  {{ card.notes }}
</div>

<div v-if="vcardUrl" class="flex items-center justify-center">
      <a
              :href="vcardUrl"
              class="inline-flex items-center px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              vCard
            </a>
</div>

  <!-- LISTA CAMPI (template flowbite) -->
          <ul class="my-6 space-y-3 text-left w-full max-w-xl mx-auto">
            <li v-for="(f, i) in visibleFields" :key="i">
              <a
                :href="hrefFor(f)"
                :target="isExternal(f) ? '_blank' : null"
                :rel="isExternal(f) ? 'noopener' : null"
                class="flex items-center p-3 text-base font-medium text-gray-900 rounded-lg bg-gray-50 hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
              >
                <!-- Icona -->
                <span class="shrink-0 h-5 w-5" v-html="iconFor(f)"></span>

                <!-- Testo -->
                <span class="flex-1 ms-3 whitespace-pre-wrap">
                  <span class="font-semibold">{{ labelFor(f) }}</span>
                  <!-- <span class="block text-sm font-normal text-gray-600 dark:text-gray-200 break-all">
                    {{ displayValue(f) }}
                  </span> -->
                </span>

                <!-- Freccia esterna se link esterno -->
                <span v-if="isExternal(f)" class="ms-2 opacity-60 group-hover:opacity-100">
                  <span class="inline-block align-middle" v-html="svgExternal()"></span>
                </span>
              </a>
            </li>
          </ul>
<!-- FINE LISTA CAMPI -->
        <div class="flex items-center justify-center">
  <img
    :src="qrUrl"
    alt="QR"
    class="w-50 h-50 rounded border border-gray-200 dark:border-gray-700"
  />
</div>

        </div>
      </div>
    </div>

    <!-- CARD ORIGINALE -->

    
    
    
    <div
      class="py-10 px-6 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-8"
    >
      <div class="grid gap-8 sm:grid-cols-1 place-items-center">
        <div class="text-center text-gray-600 dark:text-gray-300">
          <img
            v-if="card?.avatar_url"
            :src="card.avatar_url"
            class="mx-auto mb-4 w-36 h-36 rounded-full object-cover ring-4 ring-gray-200 dark:ring-gray-700"
            :alt="card?.title || 'Avatar'"
          />
          <h1
            class="mb-1 text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white"
          >
            {{ card?.title || "Contact" }}
          </h1>
          <p v-if="subtitle" class="text-base text-gray-500 dark:text-gray-400">
            {{ subtitle }}
          </p>

          <!-- Social icons -->
          <ul class="flex justify-center mt-5 space-x-4">
            <li v-for="s in socials" :key="s.type">
              <a
                :href="s.href"
                target="_blank"
                rel="noopener"
                :class="s.color"
                class="hover:opacity-90"
                aria-label="social link"
              >
                <span
                  class="w-6 h-6 inline-block align-middle"
                  v-html="s.svg"
                ></span>
              </a>
            </li>
          </ul>

          <!-- Lista campi visibili -->
          <div class="mt-6 max-w-md mx-auto text-left">
            <ul class="space-y-2">
              <li
                v-for="(f, i) in visibleFields"
                :key="i"
                class="flex items-baseline gap-2"
              >
                <strong class="text-gray-900 dark:text-white"
                  >{{ f.label || fallbackLabel(f.type) }}:</strong
                >
                <span class="break-all">{{ f.value }}</span>
              </li>
            </ul>
          </div>

          <!-- CTA -->
          <div class="mt-7 flex items-center justify-center gap-3">
            <a
              :href="vcardUrl"
              class="inline-flex items-center px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              💾 Scarica vCard
            </a>
            <img
              :src="qrUrl"
              alt="QR"
              class="w-20 h-20 rounded border border-gray-200 dark:border-gray-700"
            />
          </div>
        </div>
      </div>
    </div>





  </section>
</template>


<script setup>
import { computed } from 'vue'

const props = defineProps({
  card: { type: Object, required: true },
  vcardUrl: { type: String, required: true },
  qrUrl: { type: String, required: true },
  visibleFields: { type: Array, required: true }
})

/* Sottotitolo (role/company preferiti) */
const subtitle = computed(() => {
  const role = firstValueOf(props.visibleFields, ['role','title','job'])
  const company = firstValueOf(props.visibleFields, ['company','org','organization'])
  if (role && company) return `${role} – ${company}`
  return role || company || ''
})

/* Socials (come prima) */
const socials = computed(() => {
  const candidates = [
    social('facebook', ['facebook'], svgFacebook(), 'text-[#39569c]'),
    social('x',        ['x','twitter'], svgX(), 'text-[#00acee]'),
    social('github',   ['github'], svgGithub(), 'text-gray-900 dark:text-gray-300'),
    social('dribbble', ['dribbble'], svgDribbble(), 'text-[#ea4c89]'),
    social('linkedin', ['linkedin'], svgLinkedIn(), 'text-[#0a66c2]'),
    social('instagram',['instagram'], svgInstagram(), 'text-pink-600'),
    social('tiktok',   ['tiktok'], svgTiktok(), 'text-black dark:text-white'),
    social('youtube',  ['youtube'], svgYoutube(), 'text-red-600'),
    social('twitch',   ['twitch'], svgTwitch(), 'text-purple-600'),
    social('strava',   ['strava'], svgRun(), 'text-orange-600'),
    social('telegram', ['telegram'], svgTelegram(), 'text-sky-500'),
    social('whatsapp', ['whatsapp'], svgWhatsapp(), 'text-green-600'),
    social('website',  ['url','website','site','link'], svgLink(), 'text-gray-700 dark:text-gray-300'),
    social('email',    ['email'], svgMail(), 'text-blue-600', v => `mailto:${v}`),
  ]
  return candidates
    .map(c => {
      const val = firstValueOf(props.visibleFields, c.types)
      if (!val) return null
      return { type: c.type, href: c.toHref ? c.toHref(val) : normalizeUrl(val), svg: c.svg, color: c.color }
    })
    .filter(Boolean)
})

/* Utils base */
function social(type, types, svg, color, toHref) { return { type, types, svg, color, toHref } }
function firstValueOf(fields, types) {
  const t = types.map(s => String(s).toLowerCase())
  const f = (fields || []).find(x => t.includes(String(x.type || '').toLowerCase()) && x.value)
  return f ? f.value : ''
}
function normalizeUrl(v) {
  const s = String(v || '').trim()
  if (!s) return ''
  return /^https?:\/\//i.test(s) ? s : `https://${s}`
}

/* Label/value/href per riga */
function labelFor(f) {
  const t = (f?.type || '').toLowerCase()
  if (t === 'email') return 'Email'
  if (['mobile','phone','tel'].includes(t)) return 'Telefono'
  if (['url','website','site','link'].includes(t)) return 'Sito'
  if (['company','org','organization'].includes(t)) return 'Azienda'
  if (['role','title','job'].includes(t)) return 'Ruolo'
  if (['address','addr'].includes(t)) return 'Indirizzo'
  return f?.label || 'Info'
}
function displayValue(f) {
  return String(f?.value || '')
}
function hrefFor(f) {
  const t = (f?.type || '').toLowerCase()
  const v = String(f?.value || '').trim()
  if (!v) return '#'
  if (t === 'email') return `mailto:${v}`
  if (['mobile','phone','tel'].includes(t)) return `tel:${v.replace(/\s+/g,'')}`
  const urlLike = ['url','website','site','link','linkedin','instagram','x','twitter','facebook','github','youtube','tiktok','twitch','onlyfans','strava','telegram','whatsapp']
  if (urlLike.includes(t)) return normalizeUrl(v)
  return '#'
}
function isExternal(f) {
  const t = (f?.type || '').toLowerCase()
  if (t === 'email' || ['mobile','phone','tel'].includes(t)) return false
  return hrefFor(f) !== '#'
}

/* Icone SVG inline per ciascun tipo (stringhe) */
function iconFor(f) {
  const t = (f?.type || '').toLowerCase()
  if (t === 'email') return svgMail()
  if (['mobile','phone','tel'].includes(t)) return svgPhone()
  if (['url','website','site','link'].includes(t)) return svgLink()
  if (t === 'linkedin') return svgLinkedIn()
  if (t === 'instagram') return svgInstagram()
  if (t === 'x' || t === 'twitter') return svgX()
  if (t === 'facebook') return svgFacebook()
  if (t === 'github') return svgGithub()
  if (t === 'youtube') return svgYoutube()
  if (t === 'tiktok') return svgTiktok()
  if (t === 'twitch') return svgTwitch()
  if (t === 'onlyfans') return svgStar()
  if (t === 'strava') return svgRun()
  if (t === 'telegram') return svgTelegram()
  if (t === 'whatsapp') return svgWhatsapp()
  if (t === 'company' || t === 'org' || t === 'organization') return svgBuilding()
  if (t === 'role' || t === 'title' || t === 'job') return svgBadge()
  if (t === 'address' || t === 'addr') return svgLocation()
  return svgInfo()
}

/* SVG helper: piccole icone coerenti col template */
function svgExternal(){return `<svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M5 4a1 1 0 000 2h6.586L4.293 13.293a1 1 0 101.414 1.414L13 7.414V14a1 1 0 102 0V5a1 1 0 00-1-1H5z" clip-rule="evenodd"/></svg>`}
function svgInfo(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`}
function svgMail(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 6a2 2 0 012-2h16a2 2 0 012 2v.4L12 12.65 2 6.4V6zm0 3.333V18a2 2 0 002 2h16a2 2 0 002-2V9.333l-10 6.25-10-6.25z"/></svg>`}
function svgPhone(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1C10.3 21 3 13.7 3 4a1 1 0 011-1h2.47a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.25 1.01l-2.2 2.1z"/></svg>`}
function svgLink(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.9 12A4.1 4.1 0 018 7.9h3V6H8a6 6 0 100 12h3v-1.9H8A4.1 4.1 0 013.9 12zm7.1 1h4v-2h-4v2zm5-8h-3v1.9h3A4.1 4.1 0 0120.1 12 4.1 4.1 0 0116 16.1h-3V18h3a6 6 0 100-12z"/></svg>`}
function svgFacebook(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 5 3.66 9.13 8.44 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.77l-.44 2.89h-2.33v6.99C18.34 21.13 22 16.99 22 12z"/></svg>`}
function svgX(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.24 2.25h3.31l-7.23 8.26 8.5 11.24H16.17l-5.37-7.03-6.15 7.03H1.34l7.73-8.84L.9 2.25h6.86l4.85 6.41 5.63-6.41z"/></svg>`}
function svgGithub(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5A11.5 11.5 0 008.37 22.9c.58.1.79-.25.79-.55v-2.17c-3.19.7-3.86-1.37-3.86-1.37-.52-1.33-1.28-1.68-1.28-1.68-1.04-.72.08-.71.08-.71 1.16.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.75.4-1.25.73-1.54-2.55-.29-5.23-1.27-5.23-5.67 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a10.96 10.96 0 015.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.8 1.18 1.83 1.18 3.08 0 4.41-2.68 5.38-5.24 5.66.41.36.78 1.06.78 2.13v3.16c0 .31.21.67.8.55A11.5 11.5 0 0012 .5z"/></svg>`}
function svgDribbble(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.6 4.61a8.5 8.5 0 011.93 5.31c-.28-.05-3.1-.63-5.94-.27-.06-.14-.12-.29-.18-.45-.19-.41-.37-.83-.56-1.24 3.15-1.28 4.58-3.12 4.75-3.36zM12 3.48c2.17 0 4.15.81 5.66 2.15-.15.22-1.44 1.94-4.48 3.08C11.78 6.13 10.23 4.02 9.99 3.68A8.7 8.7 0 0112 3.48zM3.45 12.01v-.26c.37.01 4.51.06 8.78-1.22.25.48.48.97.69 1.45-.11.03-.23.07-.34.1-4.4 1.42-6.75 5.3-6.94 5.63A8.52 8.52 0 013.45 12zm8.55 8.54a8.48 8.48 0 01-5.24-1.8c.15-.32 1.89-3.66 6.7-5.34.02 0 .03-.01.05-.02.83 2.1 1.46 4.3 1.82 6.47-.42.12-.86.19-1.33.19z"/></svg>`}
function svgLinkedIn(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8.99h4V24h-4zM8.98 8.99h3.83v2.03h.05c.53-1 1.84-2.05 3.79-2.05 4.06 0 4.81 2.67 4.81 6.15V24h-4v-5.35c0-1.27-.02-2.9-1.77-2.9-1.77 0-2.04 1.38-2.04 2.81V24h-4z"/></svg>`}
function svgInstagram(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.2c3.2 0 3.58.01 4.85.07 1.17.06 1.97.24 2.43.4a4.9 4.9 0 011.77 1.16 4.9 4.9 0 011.15 1.77c.16.46.35 1.26.4 2.43.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.24 1.97-.4 2.43a4.9 4.9 0 01-1.15 1.77 4.9 4.9 0 01-1.77 1.15c-.46.16-1.26.35-2.43.4-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.97-.24-2.43-.4a4.9 4.9 0 01-1.77-1.15 4.9 4.9 0 01-1.15-1.77c-.16-.46-.35-1.26-.4-2.43C2.2 15.78 2.2 15.4 2.2 12.2s.01-3.58.07-4.85c.05-1.17.24-1.97.4-2.43A4.9 4.9 0 014.42 3.1a4.9 4.9 0 011.77-1.15c.46-.16 1.26-.35 2.43-.4C9.29 1.58 9.68 1.57 12 1.57s2.71.01 3.98.07c1.17.05 1.97.24 2.43.4a4.9 4.9 0 011.77 1.15 4.9 4.9 0 011.15 1.77c.16.46.35 1.26.4 2.43.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.24 1.97-.4 2.43a4.9 4.9 0 01-1.15 1.77 4.9 4.9 0 01-1.77 1.15c-.46.16-1.26.35-2.43.4-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.97-.24-2.43-.4a4.9 4.9 0 01-1.77-1.15 4.9 4.9 0 01-1.15-1.77c-.16-.46-.35-1.26-.4-2.43C2.21 15.78 2.2 15.4 2.2 12.2zM12 5.84a6.36 6.36 0 100 12.72 6.36 6.36 0 000-12.72zm8.4-1.1a1.49 1.49 0 11-2.98 0 1.49 1.49 0 012.98 0z"/></svg>`}
function svgTiktok(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 3h2.1c.2 1 .6 1.9 1.2 2.7.8 1.1 2 1.8 3.3 2.1v2.2c-1.3-.1-2.5-.5-3.6-1.2-.5-.3-1-.7-1.4-1.1v6.9c0 1.9-.7 3.4-2 4.5-1.3 1.2-2.8 1.7-4.5 1.5-1.7-.1-3.1-.9-4.1-2.2-.9-1.3-1.2-2.8-.9-4.4.4-1.6 1.3-2.8 2.7-3.7 1.1-.6 2.2-.8 3.5-.6v2.3c-.8-.1-1.5.1-2.1.6-.7.6-1.1 1.4-1.1 2.4 0 1 .3 1.8 1 2.4.6.6 1.4.9 2.3.9.9 0 1.7-.3 2.3-.9.7-.6 1-1.4 1-2.4V3z"/></svg>`}
function svgYoutube(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2s-.2-1.6-.8-2.2c-.8-.9-1.7-.9-2.2-1C16.9 2.5 12 2.5 12 2.5S7.1 2.5 3.5 3c-.5.1-1.4.1-2.2 1C.7 4.6.5 6.2.5 6.2S0 8.2 0 10.2v1.7c0 2 .5 4 5.3 4.5 2.2.2 4.1.3 5.7.3h.1c1.6 0 3.5-.1 5.7-.3C24 16 24.5 14 24.5 11.9V10.2c0-2-.5-4-1-4zM9.8 14.2V7.9l6.4 3.2-6.4 3.1z"/></svg>`}
function svgTwitch(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 2L2 6v14h5v2h2l2-2h4l5-5V2H4zm16 11.2l-3.1 3.1H12l-2 2H8v-2H4V4h16v9.2zM14 6h2v5h-2V6zm-5 0h2v5H9V6z"/></svg>`}
function svgRun(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 5.5a2.5 2.5 0 11.001 5.001A2.5 2.5 0 0113 5.5zM6 20l2-5 2.5-1.5-1-2.5 2-1.5 1.5 2 3 1-.5 2-2-.5-1.5 1L13 20H6z"/></svg>`}
function svgTelegram(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9.04 15.8l-.36 5.01c.51 0 .73-.22 1-.48l2.41-2.31 4.99 3.64c.92.5 1.57.24 1.81-.85l3.28-15.37c.29-1.36-.49-1.89-1.38-1.56L1.27 9.48c-1.32.51-1.3 1.25-.22 1.58l5.33 1.66 12.37-7.8c.58-.35 1.12-.16.68.2"/></svg>`}
function svgWhatsapp(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M.06 24l1.69-6.16A10.93 10.93 0 011.2 11.34C1.2 5.08 6.28 0 12.54 0 18.8 0 23.88 5.08 23.88 11.34c0 6.26-5.08 11.34-11.34 11.34-1.93 0-3.74-.48-5.34-1.33L.06 24zm6.44-4.95c1.58.94 3.4 1.42 5.28 1.42 5.6 0 10.14-4.54 10.14-10.14S17.38.19 11.78.19C6.18.19 1.64 4.73 1.64 10.33c0 1.8.51 3.5 1.39 4.96l-.9 3.3 3.37-.54zm10.28-3.18c-.07-.11-.25-.18-.52-.31-.27-.12-1.58-.78-1.82-.86-.24-.09-.42-.14-.6.14-.18.27-.69.86-.85 1.03-.16.18-.31.2-.58.07-.27-.14-1.15-.42-2.2-1.33-.81-.72-1.35-1.61-1.5-1.88-.16-.27-.02-.41.12-.54l.4-.47c.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.6-1.45-.82-1.98-.22-.53-.44-.46-.6-.47H7.4c-.18 0-.48.07-.73.34-.25.27-.96.94-.96 2.29s.99 2.66 1.13 2.85c.14.18 1.94 2.96 4.7 4.15.66.29 1.18.46 1.58.59.66.21 1.26.18 1.73.11.53-.08 1.58-.65 1.8-1.27.22-.62.22-1.15.15-1.27z"/></svg>`}
function svgBuilding(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 22V6a2 2 0 012-2h4V2h4v2h4a2 2 0 012 2v16h-6v-6H10v6H4zm6-8h4V6h-4v8z"/></svg>`}
function svgBadge(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 4h14a1 1 0 011 1v7a5 5 0 01-5 5H9a5 5 0 01-5-5V5a1 1 0 011-1zm7 2a3 3 0 100 6 3 3 0 000-6zM4 20h16v2H4z"/></svg>`}
function svgLocation(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"/></svg>`}
function svgStar(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.96 6.01L22 9.27l-5 4.87 1.18 6.86L12 17.77 5.82 21l1.18-6.86-5-4.87 7.04-1.26L12 2z"/></svg>`}
</script>
