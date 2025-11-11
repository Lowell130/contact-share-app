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

    <button class="px-4 py-2 bg-black text-white rounded">Salva</button>
  </form>
</template>

<script setup>
const FIELD_TYPES = [
  { value: 'email',     label: 'Email',      placeholder: 'nome@dominio.it' },
  { value: 'mobile',    label: 'Cellulare',  placeholder: '+39 3xx xxx xxxx' },
  { value: 'phone',     label: 'Telefono',   placeholder: '+39 0xx xxx xxxx' },
  { value: 'url',       label: 'Sito web',   placeholder: 'https://example.com' },
  { value: 'linkedin',  label: 'LinkedIn',   placeholder: 'https://www.linkedin.com/in/username' },
  { value: 'instagram', label: 'Instagram',  placeholder: 'https://instagram.com/username' },
  { value: 'x',         label: 'X (Twitter)',placeholder: 'https://x.com/username' },
  { value: 'facebook',  label: 'Facebook',   placeholder: 'https://facebook.com/username' },
  { value: 'whatsapp',  label: 'WhatsApp',   placeholder: 'https://wa.me/39333xxxxxxx' },
  { value: 'telegram',  label: 'Telegram',   placeholder: 'https://t.me/username' },
  { value: 'github',    label: 'GitHub',     placeholder: 'https://github.com/username' },
  { value: 'youtube',   label: 'YouTube',    placeholder: 'https://youtube.com/@channel' },
  { value: 'tiktok',    label: 'TikTok',     placeholder: 'https://tiktok.com/@username' },
  { value: 'twitch',    label: 'Twitch',     placeholder: 'https://twitch.tv/username' },
  { value: 'onlyfans',  label: 'OnlyFans',   placeholder: 'https://onlyfans.com/username' },
  { value: 'strava',    label: 'Strava',     placeholder: 'https://www.strava.com/athletes/12345' },
  { value: 'company',   label: 'Azienda',    placeholder: 'Ragione sociale' },
  { value: 'role',      label: 'Ruolo',      placeholder: 'es. Product Manager' },
  { value: 'address',   label: 'Indirizzo',  placeholder: 'Via Esempio 1, Roma' },
  { value: 'note',      label: 'Note',       placeholder: 'Testo libero' }
]

const defaultField = (type = 'email') => {
  const meta = FIELD_TYPES.find(t => t.value === type) || FIELD_TYPES[0]
  return { type: meta.value, label: meta.label, value: '', visible: true }
}

const props = defineProps({ modelValue: { type: Object, default: () => ({}) } })
const emit = defineEmits(['update:modelValue', 'submit'])

const form = reactive({
  title: props.modelValue.title || '',
  slug: props.modelValue.slug || '',
  bio:  props.modelValue.bio  || props.modelValue.notes || '',
  fields: Array.isArray(props.modelValue.fields) ? JSON.parse(JSON.stringify(props.modelValue.fields)) : [],
  is_public: props.modelValue.is_public ?? true,
  allow_vcard: props.modelValue.allow_vcard ?? true
})

watch(form, () => emit('update:modelValue', form), { deep: true })

const quickType = ref('email')
const addField = (type) => form.fields.push(defaultField(type))
const removeField = (i) => form.fields.splice(i, 1)

const placeholderFor = (f) => {
  const meta = FIELD_TYPES.find(t => t.value === (f?.type || '')) || FIELD_TYPES[0]
  return { label: meta.label, value: meta.placeholder }
}

const applyTypeDefaults = (f) => {
  const meta = FIELD_TYPES.find(t => t.value === (f?.type || ''))
  if (!meta) return
  if (!f.label || f.label.trim() === '' || FIELD_TYPES.some(t => t.label === f.label)) {
    f.label = meta.label
  }
}

const normalizeValue = (f) => {
  const v = (f.value || '').trim()
  const type = (f.type || '').toLowerCase()
  const urlLike = [
    'url','linkedin','instagram','x','facebook','whatsapp','telegram',
    'github','youtube','tiktok','twitch','onlyfans','strava'
  ]
  if (v && urlLike.includes(type)) {
    f.value = /^https?:\/\//i.test(v) ? v : `https://${v}`
  } else {
    f.value = v
  }
}

const onSubmit = () => {
  const cleaned = {
    title: (form.title || '').trim(),
    slug: (form.slug || '').trim(),
    notes: (form.bio || '').trim(),
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
