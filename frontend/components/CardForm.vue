<template>
  <form @submit.prevent="onSubmit" class="space-y-6 max-w-3xl">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">Titolo/Nome</label>
        <input v-model="form.title" class="border p-2 w-full rounded" required />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Slug (opz.)</label>
        <input v-model="form.slug" class="border p-2 w-full rounded" placeholder="es. stefano" />
      </div>
      <div class="md:col-span-2">
        <label class="block text-sm font-medium mb-1">Bio (breve)</label>
        <textarea
          v-model="form.bio"
          class="border p-2 w-full rounded"
          rows="3"
          placeholder="Breve presentazione/claim sotto al titolo…"
        />
      </div>
      
    </div>

    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <label class="text-sm font-medium">Campi</label>
        <div class="flex gap-2">
          <select v-model="quickType" class="border p-2 rounded">
            <option disabled value="">Aggiungi rapido…</option>
            <option v-for="opt in FIELD_TYPES" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
          <button type="button" @click="addField(quickType || 'email')" class="px-3 py-2 border rounded">
            + Aggiungi
          </button>
        </div>
      </div>

      <div v-if="!form.fields.length" class="text-sm text-gray-500">Nessun campo. Usa “Aggiungi”.</div>

      <div
        v-for="(f, i) in form.fields"
        :key="i"
        class="grid grid-cols-12 gap-2 items-center border rounded p-3"
      >
        <div class="col-span-12 md:col-span-3">
          <label class="block text-xs font-medium mb-1">Tipo</label>
          <select v-model="f.type" @change="applyTypeDefaults(f)" class="border p-2 w-full rounded">
            <option v-for="opt in FIELD_TYPES" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="col-span-12 md:col-span-3">
          <label class="block text-xs font-medium mb-1">Label</label>
          <input v-model="f.label" class="border p-2 w-full rounded" :placeholder="placeholderFor(f).label" />
        </div>
        <div class="col-span-12 md:col-span-5">
          <label class="block text-xs font-medium mb-1">Valore</label>
          <input
            v-model="f.value"
            @blur="normalizeValue(f)"
            class="border p-2 w-full rounded"
            :placeholder="placeholderFor(f).value"
          />
        </div>
        <div class="col-span-12 md:col-span-1 flex md:block items-center justify-between gap-3">
          <label class="inline-flex items-center gap-2 text-xs">
            <input type="checkbox" v-model="f.visible" />
            visibile
          </label>
          <button type="button" @click="removeField(i)" class="text-red-600 text-xs">rimuovi</button>
        </div>
      </div>
    </div>

    <div class="flex flex-wrap gap-4">
      <label class="inline-flex items-center gap-2">
        <input type="checkbox" v-model="form.is_public" />
        Pubblica
      </label>
      <label class="inline-flex items-center gap-2">
        <input type="checkbox" v-model="form.allow_vcard" />
        Consenti vCard
      </label>
    </div>

    <!-- aggiungi subito sopra il bottone Salva -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div>
    <label class="block text-sm font-medium mb-1">Tema grafico</label>
    <select v-model="form.theme" class="border p-2 w-full rounded">
      <option disabled value="">Scegli un tema...</option>
      <option value="minimal">Minimal</option>
      <option value="gradient">Colorful Gradient</option>
      <option value="dark">Dark Tech</option>
      <option value="flowbite">Flowbite Card</option> <!-- NEW -->
    </select>
  </div>
</div>


    <button class="px-4 py-2 bg-black text-white rounded">Salva</button>
  </form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'

/* --------------------------------
 * CONFIG UNICA PER I CAMPI
 * -------------------------------- */
const FIELD_CONFIG = {
  email: {
    label: 'Email',
    placeholder: 'nome@dominio.it',
    urlLike: false
  },
  mobile: {
    label: 'Cellulare',
    placeholder: '+39 3xx xxx xxxx',
    urlLike: false
  },
  phone: {
    label: 'Telefono',
    placeholder: '+39 0xx xxx xxxx',
    urlLike: false
  },
  url: {
    label: 'Sito web',
    placeholder: 'https://example.com',
    urlLike: true
  },
  linkedin: {
    label: 'LinkedIn',
    placeholder: 'https://www.linkedin.com/in/username',
    urlLike: true
  },
  instagram: {
    label: 'Instagram',
    placeholder: 'https://instagram.com/username',
    urlLike: true
  },
  x: {
    label: 'X (Twitter)',
    placeholder: 'https://x.com/username',
    urlLike: true
  },
  facebook: {
    label: 'Facebook',
    placeholder: 'https://facebook.com/username',
    urlLike: true
  },
  whatsapp: {
    label: 'WhatsApp',
    placeholder: 'https://wa.me/39333xxxxxxx',
    urlLike: true
  },
  telegram: {
    label: 'Telegram',
    placeholder: 'https://t.me/username',
    urlLike: true
  },
  github: {
    label: 'GitHub',
    placeholder: 'https://github.com/username',
    urlLike: true
  },
  youtube: {
    label: 'YouTube',
    placeholder: 'https://youtube.com/@channel',
    urlLike: true
  },
  tiktok: {
    label: 'TikTok',
    placeholder: 'https://tiktok.com/@username',
    urlLike: true
  },
  twitch: {
    label: 'Twitch',
    placeholder: 'https://twitch.tv/username',
    urlLike: true
  },
  onlyfans: {
    label: 'OnlyFans',
    placeholder: 'https://onlyfans.com/username',
    urlLike: true
  },
  strava: {
    label: 'Strava',
    placeholder: 'https://www.strava.com/athletes/12345',
    urlLike: true
  },
  company: {
    label: 'Azienda',
    placeholder: 'Ragione sociale',
    urlLike: false
  },
  role: {
    label: 'Ruolo',
    placeholder: 'es. Product Manager',
    urlLike: false
  },
  address: {
    label: 'Indirizzo',
    placeholder: 'Via Esempio 1, Roma',
    urlLike: false
  },
  note: {
    label: 'Note',
    placeholder: 'Testo libero',
    urlLike: false
  }
}

// helper per recuperare meta in modo sicuro
function getFieldMeta(type) {
  const key = String(type || '').toLowerCase()
  return FIELD_CONFIG[key] || FIELD_CONFIG.email
}

// array per il <select> (usa la config)
const FIELD_TYPES = Object.entries(FIELD_CONFIG).map(([value, meta]) => ({
  value,
  label: meta.label,
  placeholder: meta.placeholder
}))

// campo di default
const defaultField = (type = 'email') => {
  const meta = getFieldMeta(type)
  return {
    type,
    label: meta.label,
    value: '',
    visible: true
  }
}

/* --------------------------------
 * PROPS / EMIT / FORM
 * -------------------------------- */
const props = defineProps({
  modelValue: { type: Object, default: () => ({}) }
})
const emit = defineEmits(['update:modelValue', 'submit'])

const form = reactive({
  title: props.modelValue.title || '',
  slug: props.modelValue.slug || '',
  bio:  props.modelValue.bio  || props.modelValue.notes || '',
  theme: props.modelValue.theme || 'minimal',
  fields: Array.isArray(props.modelValue.fields)
    ? JSON.parse(JSON.stringify(props.modelValue.fields))
    : [],
  is_public: props.modelValue.is_public ?? true,
  allow_vcard: props.modelValue.allow_vcard ?? true
})

watch(form, () => emit('update:modelValue', form), { deep: true })

/* --------------------------------
 * GESTIONE CAMPI
 * -------------------------------- */
const quickType = ref('email')

const addField = (type) => {
  form.fields.push(defaultField(type))
}

const removeField = (i) => {
  form.fields.splice(i, 1)
}

const placeholderFor = (f) => {
  const meta = getFieldMeta(f?.type)
  return {
    label: meta.label,
    value: meta.placeholder
  }
}

const applyTypeDefaults = (f) => {
  const meta = getFieldMeta(f?.type)
  if (!meta) return

  // se la label è vuota o è una label "standard", la rimpiazziamo
  if (
    !f.label ||
    f.label.trim() === '' ||
    FIELD_TYPES.some(t => t.label === f.label)
  ) {
    f.label = meta.label
  }
}

// normalizzazione valori (aggiunta https:// per i campi urlLike)
const normalizeValue = (f) => {
  const v = (f.value || '').trim()
  const meta = getFieldMeta(f?.type)

  if (v && meta.urlLike) {
    f.value = /^https?:\/\//i.test(v) ? v : `https://${v}`
  } else {
    f.value = v
  }
}

/* --------------------------------
 * SUBMIT
 * -------------------------------- */
const onSubmit = () => {
  const cleaned = {
    title: (form.title || '').trim(),
    slug: (form.slug || '').trim(),
    notes: (form.bio || '').trim(),
    theme: (form.theme || 'minimal'),
    is_public: !!form.is_public,
    allow_vcard: !!form.allow_vcard,
    fields: (form.fields || [])
      .filter(x => x && typeof x === 'object')
      .map(x => ({
        type: (x.type || '').toLowerCase(),
        label: (x.label || '').trim(),
        value: (x.value || '').trim(),
        visible: x.visible !== false
      }))
      .filter(x => x.type && x.value)
  }

  emit('submit', cleaned)
}
</script>
