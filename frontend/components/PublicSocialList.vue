<!-- components/PublicSocialList.vue -->
<template>
  <ul
    v-if="socialFields.length"
    class="my-6 space-y-3 text-left w-full max-w-xl mx-auto"
  >
    <li v-for="(f, i) in socialFields" :key="i">
      <a
        :href="hrefFor(f)"
        :target="isExternal(f) ? '_blank' : null"
        :rel="isExternal(f) ? 'noopener' : null"
        :aria-label="`Apri ${socialLabelFor(f)} di ${cardTitle}`"
        :class="[
          // base + effetto glass
          'flex items-center p-3 text-base font-medium rounded-xl group',
          'border border-white/10',
          'transition duration-200 ease-out transform',
          'hover:-translate-y-0.5 hover:shadow-xl',
          'hover:border-white/40 hover:backdrop-blur-sm',
          socialClassFor(f)
        ]"
        @click="onClickSocial(f)"
      >
        <!-- Icona -->
        <span class="shrink-0 h-5 w-5" v-html="iconFor(f)"></span>

        <!-- Label -->
        <span class="flex-1 ms-3 whitespace-pre-wrap">
          <span class="font-semibold">
            {{ socialLabelFor(f) }}
          </span>
        </span>

        <!-- Freccia esterna -->
        <span v-if="isExternal(f)" class="ms-2 opacity-80 group-hover:opacity-100">
          <span class="inline-block align-middle" v-html="svgExternal()"></span>
        </span>
      </a>
    </li>
  </ul>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  cardTitle: { type: String, default: '' },
  cardId:    { type: String, required: true },
  fields:    { type: Array, required: true }
})

const config = useRuntimeConfig()

/* -----------------------------
 *  CONFIG SOCIAL + GRADIENT
 * ----------------------------- */
const SOCIAL_CONFIG = {
  facebook: {
    label: 'Facebook',
    bg: 'bg-gradient-to-r from-[#1877F2] to-[#0F5AC6]',
    icon: svgFacebook,
  },
  instagram: {
    label: 'Instagram',
    bg: 'bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500',
    icon: svgInstagram,
  },
  linkedin: {
    label: 'LinkedIn',
    bg: 'bg-gradient-to-r from-[#0A66C2] to-[#004182]',
    icon: svgLinkedIn,
  },
  x: {
    label: 'X',
    bg: 'bg-gradient-to-r from-gray-900 to-black',
    icon: svgX,
  },
  twitter: {
    label: 'X', // alias
    bg: 'bg-gradient-to-r from-gray-900 to-black',
    icon: svgX,
  },
  github: {
    label: 'GitHub',
    bg: 'bg-gradient-to-r from-gray-900 to-gray-700',
    icon: svgGithub,
  },
  youtube: {
    label: 'YouTube',
    bg: 'bg-gradient-to-r from-[#FF0000] to-[#CC0000]',
    icon: svgYoutube,
  },
  tiktok: {
    label: 'TikTok',
    bg: 'bg-gradient-to-r from-black via-slate-900 to-black',
    icon: svgTiktok,
  },
  twitch: {
    label: 'Twitch',
    bg: 'bg-gradient-to-r from-[#9146FF] to-[#772CE8]',
    icon: svgTwitch,
  },
  strava: {
    label: 'Strava',
    bg: 'bg-gradient-to-r from-[#FC4C02] to-[#D84301]',
    icon: svgRun,
  },
  telegram: {
    label: 'Telegram',
    bg: 'bg-gradient-to-r from-[#229ED9] to-[#146A9E]',
    icon: svgTelegram,
  },
  whatsapp: {
    label: 'WhatsApp',
    bg: 'bg-gradient-to-r from-[#25D366] to-[#128C7E]',
    icon: svgWhatsapp,
  },
  onlyfans: {
    label: 'OnlyFans',
    bg: 'bg-gradient-to-r from-[#00AFF0] to-[#0085B8]',
    icon: svgStar,
  },
  dribbble: {
    label: 'Dribbble',
    bg: 'bg-gradient-to-r from-[#EA4C89] to-[#C2185B]',
    icon: svgDribbble,
  },
}

const SOCIAL_TYPES = Object.keys(SOCIAL_CONFIG)

/* -----------------------------
 *  SOCIAL FIELDS
 * ----------------------------- */
const socialFields = computed(() =>
  (props.fields || []).filter(
    f =>
      SOCIAL_TYPES.includes(String(f.type || '').toLowerCase()) &&
      f.value &&
      f.visible !== false
  )
)

/* -----------------------------
 *  HELPERS
 * ----------------------------- */

function normalizeUrl(v) {
  const s = String(v || '').trim()
  if (!s) return ''
  return /^https?:\/\//i.test(s) ? s : `https://${s}`
}

function socialLabelFor(f) {
  const t = (f?.type || '').toLowerCase()
  return SOCIAL_CONFIG[t]?.label || f.label || 'Social'
}

function socialClassFor(f) {
  const t = (f?.type || '').toLowerCase()
  const base = 'text-white hover:opacity-95 hover:brightness-110 dark:text-white'
  const bg = SOCIAL_CONFIG[t]?.bg

  if (bg) {
    // gradient + leggero boost luce in hover
    return `${bg} ${base}`
  }

  // fallback neutro (senza vetro, ma comunque carino)
  return 'bg-gray-50 text-gray-900 hover:bg-gray-100 dark:bg-gray-600 dark:text-white'
}

function hrefFor(f) {
  const t = (f?.type || '').toLowerCase()
  const v = String(f?.value || '').trim()
  if (!v) return '#'

  const urlLike = [
    'facebook','instagram','linkedin','x','twitter','github','youtube',
    'tiktok','twitch','strava','telegram','whatsapp','onlyfans',
    'dribbble','url','website','site','link'
  ]

  if (urlLike.includes(t)) return normalizeUrl(v)
  if (t === 'email') return `mailto:${v}`
  if (['mobile','phone','tel'].includes(t)) return `tel:${v.replace(/\s+/g, '')}`
  return '#'
}

function isExternal(f) {
  const t = (f?.type || '').toLowerCase()
  if (t === 'email' || ['mobile','phone','tel'].includes(t)) return false
  return hrefFor(f) !== '#'
}

function iconFor(f) {
  const t = (f?.type || '').toLowerCase()
  const iconFn = SOCIAL_CONFIG[t]?.icon
  return iconFn ? iconFn() : svgInfo()
}

/* -----------------------------
 *  LOG CLICK SOCIAL
 * ----------------------------- */

const onClickSocial = (f) => {
  const socialType = (f?.type || '').toLowerCase()
  const target = hrefFor(f)

  // fire & forget, non blocchiamo la navigazione
  if (!props.cardId || !socialType) return

  $fetch(`${config.public.apiBase}/public/events/social-click`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      card_id: props.cardId,
      social_type: socialType,
      target
    }
  }).catch((err) => {
    // log semplice in console, nessun impatto sulla UX
    console.warn('Errore logging social-click', err)
  })
}

/* -----------------------------
 *  SVG
 * ----------------------------- */

function svgExternal() {
  return `<svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M5 4a1 1 0 000 2h6.586L4.293 13.293a1 1 0 101.414 1.414L13 7.414V14a1 1 0 102 0V5a1 1 0 00-1-1H5z" clip-rule="evenodd"/></svg>`
}
function svgInfo() {
  return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`
}

function svgFacebook(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 5 3.66 9.13 8.44 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.77l-.44 2.89h-2.33v6.99C18.34 21.13 22 16.99 22 12z"/></svg>`}

function svgX(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.24 2.25h3.31l-7.23 8.26 8.5 11.24H16.17l-5.37-7.03-6.15 7.03H1.34l7.73-8.84L.9 2.25h6.86l4.85 6.41 5.63-6.41z"/></svg>`}

function svgGithub(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5A11.5 11.5 0 008.37 22.9c.58.1.79-.25.79-.55v-2.17c-3.19.7-3.86-1.37-3.86-1.37-.52-1.33-1.28-1.68-1.28-1.68-1.04-.72.08-.71.08-.71 1.16.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.75.4-1.25.73-1.54-2.55-.29-5.23-1.27-5.23-5.67 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a10.96 10.96 0 015.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.8 1.18 1.83 1.18 3.08 0 4.41-2.68 5.38-5.24 5.66.41.36.78 1.06.78 2.13v3.16c0 .31.21.67.8.55A11.5 11.5 0 0012 .5z"/></svg>`}

function svgDribbble(){return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.6 4.61a8.5 8.5 0 011.93 5.31c-.28-.05-3.1-.63-5.94-.27-.06-.14-.12-.29-.18-.45-.19-.41-.37-.83-.56-1.24 3.15-1.28 4.58-3.12 4.75-3.36zM12 3.48c2.17 0 4.15.81 5.66 2.15-.15.22-1.44 1.94-4.48 3.08C11.78 6.13 10.23 4.02 9.99 3.68A8.7 8.7 0 0112 3.48zM3.45 12.01v-.26c.37.01 4.51.06 8.78-1.22.25.48.48.97.69 1.45-.11.03-.23.07-.34.1-4.4 1.42-6.75 5.3-6.94 5.63A8.52 8.52 0 013.45 12zm8.55 8.54a8.48 8.48 0 01-5.24-1.8c.15-.32 1.89-3.66 6.7-5.34.02 0 .03-.01.05-.02.83 2.1 1.46 4.3 1.82 6.47-.42.12-.86.19-1.33.19z"/></svg>`}

function svgLinkedIn() {
  return `
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 24 24"
     width="24" height="24"
     fill="currentColor">
  <path fill-rule="evenodd"
    d="M12.51 8.796v1.697a3.738 3.738 0 0 1 3.288-1.684c3.455 0 4.202 2.16 4.202 4.97V19.5h-3.2v-5.072c0-1.21-.244-2.766-2.128-2.766-1.827 0-2.139 1.317-2.139 2.676V19.5h-3.19V8.796h3.168ZM7.2 6.106a1.61 1.61 0 0 1-.988 1.483 1.595 1.595 0 0 1-1.743-.348A1.607 1.607 0 0 1 5.6 4.5a1.601 1.601 0 0 1 1.6 1.606Z"
    clip-rule="evenodd"/>
  <path d="M7.2 8.809H4V19.5h3.2V8.809Z"/>
</svg>
`
}

function svgInstagram() {
  return `
<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 24 24" 
     fill="none" 
     width="24" height="24">
  <path fill="currentColor" fill-rule="evenodd"
    d="M3 8a5 5 0 0 1 5-5h8a5 5 0 0 1 5 5v8a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5V8Zm5-3a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3H8Zm7.597 2.214a1 1 0 0 1 1-1h.01a1 1 0 1 1 0 2h-.01a1 1 0 0 1-1-1ZM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm-5 3a5 5 0 1 1 10 0 5 5 0 0 1-10 0Z"
    clip-rule="evenodd"/>
</svg>
`
}

function svgTiktok() {
  return `
 <svg class="icon" viewBox="0 0 256 256"
       fill="#ffffff"
       xmlns="http://www.w3.org/2000/svg"
       aria-hidden="true">
    <path d="M232,84v40a7.99977,7.99977,0,0,1-8,8,103.32406,103.32406,0,0,1-48.00049-11.70752L176,156A76,76,0,1,1,86.59766,81.17971,7.99952,7.99952,0,0,1,96,89.05569l-.00049,41.63916a7.99971,7.99971,0,0,1-4.56689,7.22607A20.00272,20.00272,0,1,0,120,156V28a7.99977,7.99977,0,0,1,8-8h40a7.99977,7.99977,0,0,1,8,8,48.05436,48.05436,0,0,0,48,48A7.99977,7.99977,0,0,1,232,84Z"/>
  </svg>
`
}

function svgYoutube() {
  return `
<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill-rule="evenodd" d="M21.7 8.037a4.26 4.26 0 0 0-.789-1.964 2.84 2.84 0 0 0-1.984-.839c-2.767-.2-6.926-.2-6.926-.2s-4.157 0-6.928.2a2.836 2.836 0 0 0-1.983.839 4.225 4.225 0 0 0-.79 1.965 30.146 30.146 0 0 0-.2 3.206v1.5a30.12 30.12 0 0 0 .2 3.206c.094.712.364 1.39.784 1.972.604.536 1.38.837 2.187.848 1.583.151 6.731.2 6.731.2s4.161 0 6.928-.2a2.844 2.844 0 0 0 1.985-.84 4.27 4.27 0 0 0 .787-1.965 30.12 30.12 0 0 0 .2-3.206v-1.516a30.672 30.672 0 0 0-.202-3.206Zm-11.692 6.554v-5.62l5.4 2.819-5.4 2.801Z" clip-rule="evenodd"/>
</svg>
`
}

function svgTwitch() {
  return `
<svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M4.5 1L2 3.5v9h3V15l2.5-2.5h2L14 8V1H4.5zM13 7.5l-2 2H9l-1.75 1.75V9.5H5V2h8v5.5z"/>
  <path d="M11.5 3.75h-1v3h1v-3zm-2.75 0h-1v3h1v-3z"/>
</svg>
`
}

function svgRun() {
  return `
<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7 13.828h4.169"/>
</svg>
`
}

function svgTelegram(){
  return `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9.04 15.8l-.36 5.01c.51 0 .73-.22 1-.48l2.41-2.31 4.99 3.64c.92.5 1.57.24 1.81-.85l3.28-15.37c.29-1.36-.49-1.89-1.38-1.56L1.27 9.48c-1.32.51-1.3 1.25-.22 1.58l5.33 1.66 12.37-7.8c.58-.35 1.12-.16.68.2"/></svg>`
}

function svgWhatsapp() {
  return `
<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill-rule="evenodd" d="M12 4a8 8 0 0 0-6.895 12.06l.569.718-.697 2.359 2.32-.648.379.243A8 8 0 1 0 12 4ZM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10a9.96 9.96 0 0 1-5.016-1.347l-4.948 1.382 1.426-4.829-.006-.007-.033-.055A9.958 9.958 0 0 1 2 12Z" clip-rule="evenodd"/>
  <path d="M16.735 13.492c-.038-.018-1.497-.736-1.756-.83a1.008 1.008 0 0 0-.34-.075c-.196 0-.362.098-.49.291-.146.217-.587.732-.723.886-.018.02-.042.045-.057.045-.013 0-.239-.093-.307-.123-1.564-.68-2.751-2.313-2.914-2.589-.023-.04-.024-.057-.024-.057.005-.021.058-.074.085-.101.08-.079.166-.182.249-.283l.117-.14c.121-.14.175-.25.237-.375l.033-.066a.68.68 0 0 0-.02-.64c-.034-.069-.65-1.555-.715-1.711-.158-.377-.366-.552-.655-.552-.027 0 0 0-.112.005-.137.005-.883.104-1.213.311-.35.22-.94.924-.94 2.16 0 1.112.705 2.162 1.008 2.561l.041.06c1.161 1.695 2.608 2.951 4.074 3.537 1.412.564 2.081.63 2.461.63.16 0 .288-.013.4-.024l.072-.007c.488-.043 1.56-.599 1.804-1.276.192-.534.243-1.117.115-1.329-.088-.144-.239-.216-.43-.308Z"/>
</svg>
`
}

function svgStar() {
  return `
<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" width="24" height="24">
  <path d="M24 4.003h-4.015c-3.45 0-5.3.197-6.748 1.957a7.996 7.996 0 1 0 2.103 9.211c3.182-.231 5.39-2.134 6.085-5.173c0 0-2.399.585-4.43 0c4.018-.777 6.333-3.037 7.005-5.995zM5.61 11.999A2.391 2.391 0 0 1 9.28 9.97a2.966 2.966 0 0 1 2.998-2.528h.008c-.92 1.778-1.407 3.352-1.998 5.263A2.392 2.392 0 0 1 5.61 12Zm2.386-7.996a7.996 7.996 0 1 0 7.996 7.996a7.996 7.996 0 0 0-7.996-7.996Zm0 10.394A2.399 2.399 0 1 1 10.395 12a2.396 2.396 0 0 1-2.399 2.398Z"/>
</svg>`
}
</script>
