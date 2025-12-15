<!-- frontend/components/CardForm.vue  -->
<template>
  <form @submit.prevent="onSubmit" class="space-y-6 max-w-6xl">
    <!-- Avatar Upload Section -->
    <div class="flex items-center gap-6 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
      <div class="relative w-24 h-24 rounded-full bg-gray-100 overflow-hidden border border-gray-200 group flex-shrink-0">
        <img
          v-if="form.avatar_url"
          :src="resolveAvatar(form.avatar_url)"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        
        <!-- Overlay for upload -->
        <label v-if="cardId" class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity text-white text-xs font-medium">
          Change
          <input type="file" class="hidden" accept="image/*" @change="onFileSelect" />
        </label>
      </div>
      
      <div class="flex-1">
        <h3 class="text-lg font-medium text-gray-900">Avatar</h3>
        <p v-if="!cardId" class="text-sm text-gray-500 mt-1">
          Save the card to upload a custom image.
          <br>An automatic avatar will be generated if you don't upload one.
        </p>
        <div v-else class="mt-1">
          <p class="text-sm text-gray-500">
            Click on the image to upload a new one.
            <br>Supported formats: JPG, PNG, WEBP.
          </p>
          <button 
            v-if="hasCustomAvatar"
            type="button"
            @click="deleteAvatar"
            class="mt-2 text-xs text-red-600 hover:text-red-800 font-medium flex items-center gap-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Remove custom avatar
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block mb-2.5 text-sm font-medium text-heading">Title/Name</label>
        <input
          v-model="form.title"
          class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
          required
        />
      </div>
      <div>
        <label class="block mb-2.5 text-sm font-medium text-heading">Slug (opt.)</label>
        <input
          v-model="form.slug"
          class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
          placeholder="e.g. John Doe"
        />
      </div>
      <div class="md:col-span-2">
        <label class="block mb-2.5 text-sm font-medium text-heading">Bio (short)</label>
        <textarea
          v-model="form.bio"
          class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full p-3.5 shadow-xs placeholder:text-body"
          rows="3"
          placeholder="Short presentation/claim under the title…"
        />
      </div>
    </div>

    <div class="space-y-3">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <label class="block text-sm font-medium text-heading">Fields</label>

        <!-- 🔹 Select, +Aggiungi e Salva affiancati -->
        <div class="flex flex-wrap gap-2 w-full md:w-auto justify-center md:justify-start">
          <select
            v-model="quickType"
            class="block pe-8 py-2.5 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body w-full md:w-auto"
          >
            <option disabled value="">Add field</option>
            <option
              v-for="opt in FIELD_TYPES"
              :key="opt.value"
              :value="opt.value"
              :disabled="form.fields.some(f => f.type === opt.value)"
            >
              {{ opt.label }}
            </option>
          </select>

          <button
            type="button"
            @click="addField(quickType || 'email')"
            class="text-white bg-warning box-border border border-transparent hover:bg-warning-strong focus:ring-4 focus:ring-warning-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            <span>Add</span>
          </button>

          <button
            type="button"
            class="text-white bg-danger box-border border border-transparent hover:bg-danger-strong focus:ring-4 focus:ring-danger-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Reset</span>
          </button>
          <!-- 🟢 Bottone Salva spostato qui -->
          <button
            type="submit"
            class="text-white bg-success box-border border border-transparent hover:bg-success-strong focus:ring-4 focus:ring-success-medium shadow-xs font-medium leading-5 rounded-full text-sm px-4 py-2.5 focus:outline-none flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            <span>Save</span>
          </button>
        </div>
      </div>

      <div v-if="!form.fields.length" class="text-sm text-gray-500">
        No fields. Use “Add”.
      </div>

      <div
        v-for="(f, i) in form.fields"
        :key="i"
        class="grid grid-cols-12 gap-2 items-center shadow-sm rounded border border-gray-200 p-4"
      >
        <div class="col-span-12 md:col-span-3">
          <label class="block mb-2.5 text-sm font-medium text-heading">Type</label>
          <select
            v-model="f.type"
            @change="applyTypeDefaults(f)"
            class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
          >
            <option v-for="opt in FIELD_TYPES" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <div class="col-span-12 md:col-span-3">
          <label class="block mb-2.5 text-sm font-medium text-heading">Label</label>
          <input
            v-model="f.label"
            class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
            :placeholder="placeholderFor(f).label"
          />
        </div>

        <div class="col-span-12 md:col-span-5">
          <label class="block mb-2.5 text-sm font-medium text-heading">Value</label>
          <input
            v-model="f.value"
            @blur="normalizeValue(f)"
            class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
            :placeholder="placeholderFor(f).value"
          />
        </div>

        <div
          class="col-span-12 md:col-span-1
                 flex items-center justify-between gap-3
                 md:flex-col md:items-end md:justify-center"
        >
          <!-- Checkbox stile Flowbite -->
          <label class="flex items-center select-none text-xs font-medium text-heading">
            <input
              type="checkbox"
              v-model="f.visible"
              class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium
                     focus:ring-2 focus:ring-brand-soft cursor-pointer"
            />
            <span class="ms-2">Visible</span>
          </label>

          <!-- Bottone rimuovi -->
          <button
            type="button"
            @click="removeField(i)"
            class="flex items-center justify-center
                   w-7 h-7
                   bg-red-500 hover:bg-red-600
                   text-white rounded-full
                   border border-transparent
                   shadow-xs
                   focus:ring-4 focus:ring-red-300
                   focus:outline-none"
            title="Remove"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-3 h-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="3"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="flex flex-wrap gap-6">
      <div class="w-full">
        <label class="block mb-2.5 text-sm font-medium text-heading">Visibility</label>
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" v-model="visibilityMode" value="private" class="w-4 h-4 text-brand focus:ring-brand border-gray-300" />
            <span class="text-sm text-heading">Private (No one can see it)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" v-model="visibilityMode" value="public_noindex" class="w-4 h-4 text-brand focus:ring-brand border-gray-300" />
            <span class="text-sm text-heading">Public (Only those with the link, no search engines)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" v-model="visibilityMode" value="public_indexed" class="w-4 h-4 text-brand focus:ring-brand border-gray-300" />
            <span class="text-sm text-heading">Public (Indexed on Google/Bing)</span>
          </label>
        </div>
      </div>

      <label class="flex items-center select-none text-sm font-medium text-heading gap-2">
        <input
          type="checkbox"
          v-model="form.allow_vcard"
          class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium focus:ring-2 focus:ring-brand-soft cursor-pointer"
        />
        <span>Allow vCard</span>
      </label>
    </div>

    <!-- Tema grafico -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block mb-2.5 text-sm font-medium text-heading">Theme</label>
        <select
          v-model="form.theme"
          class="block w-full px-3 py-2.5 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body"
        >
          <option disabled value="">Choose a theme...</option>
          <option value="minimal">Minimal (Free)</option>
          <option value="gradient">Gradient (Free)</option>
          <option value="dark">Dark (Free)</option>
          <option value="flowbite">Flowbite (Free)</option>
          <optgroup label="Modern (Pro Only)">
            <option value="modern_emerald" :disabled="!isPro">Modern Emerald {{ !isPro ? '🔒' : '' }}</option>
            <option value="modern_blue" :disabled="!isPro">Modern Blue {{ !isPro ? '🔒' : '' }}</option>
            <option value="modern_indigo" :disabled="!isPro">Modern Indigo {{ !isPro ? '🔒' : '' }}</option>
            <option value="modern_rose" :disabled="!isPro">Modern Rose {{ !isPro ? '🔒' : '' }}</option>
            <option value="modern_orange" :disabled="!isPro">Modern Orange {{ !isPro ? '🔒' : '' }}</option>
          </optgroup>
        </select>
        <div class="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100 flex items-center justify-between">
        <div>
           <p class="text-sm text-blue-800 font-medium">Upgrade to Pro</p>
           <p class="text-xs text-blue-600">Unlock all premium themes and more.</p>
        </div>
        <button 
          type="button"
          @click="upgradeToPro"
          class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold py-2 px-4 rounded-full transition-colors"
        >
          Try Pro
        </button>
      </div>
      </div>
    </div>

    <!-- 🔻 vecchio bottone Salva rimosso da qui -->
  </form>
</template>

<script setup>
import { reactive, ref, watch, computed } from 'vue'

const { user } = useAuth()
const isPro = computed(() => user.value?.plan === 'pro' || user.value?.plan === 'admin')

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
    label: 'Mobile',
    placeholder: '+39 3xx xxx xxxx',
    urlLike: false
  },
  phone: {
    label: 'Phone',
    placeholder: '+39 0xx xxx xxxx',
    urlLike: false
  },
  url: {
    label: 'Website',
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
    urlLike: true,
    prefix: 'https://wa.me/'
  },
  telegram: {
    label: 'Telegram',
    placeholder: 'https://t.me/username',
    urlLike: true,
    prefix: 'https://t.me/'
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
    label: 'Company',
    placeholder: 'Company Name',
    urlLike: false
  },
  role: {
    label: 'Role',
    placeholder: 'e.g. Product Manager',
    urlLike: false
  },
  address: {
    label: 'Address',
    placeholder: '123 Example St, City',
    urlLike: false
  },
  note: {
    label: 'Notes',
    placeholder: 'Free text',
    urlLike: false
  }
}

function getFieldMeta (type) {
  const key = String(type || '').toLowerCase()
  return FIELD_CONFIG[key] || FIELD_CONFIG.email
}

const FIELD_TYPES = Object.entries(FIELD_CONFIG).map(([value, meta]) => ({
  value,
  label: meta.label,
  placeholder: meta.placeholder
}))

const defaultField = (type = 'email') => {
  const meta = getFieldMeta(type)
  return {
    type,
    label: meta.label,
    value: meta.prefix || '',
    visible: true
  }
}

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  cardId: { type: String, default: null }
})
const emit = defineEmits(['update:modelValue', 'submit'])

const form = reactive({
  title: props.modelValue.title || '',
  slug: props.modelValue.slug || '',
  bio: props.modelValue.bio || props.modelValue.notes || '',
  theme: props.modelValue.theme || 'minimal',
  avatar_url: props.modelValue.avatar_url || '',
  fields: Array.isArray(props.modelValue.fields)
    ? JSON.parse(JSON.stringify(props.modelValue.fields))
    : [],
  is_public: props.modelValue.is_public ?? true,
  is_indexed: props.modelValue.is_indexed ?? true,
  allow_vcard: props.modelValue.allow_vcard ?? true
})

const visibilityMode = computed({
  get() {
    if (!form.is_public) return 'private'
    return form.is_indexed ? 'public_indexed' : 'public_noindex'
  },
  set(val) {
    if (val === 'private') {
      form.is_public = false
      form.is_indexed = false // doesn't matter much, but cleaner
    } else if (val === 'public_noindex') {
      form.is_public = true
      form.is_indexed = false
    } else {
      form.is_public = true
      form.is_indexed = true
    }
  }
})

watch(form, () => emit('update:modelValue', form), { deep: true })

const quickType = ref('email')

const addField = (type) => {
  if (!type) return
  if (form.fields.some(f => f.type === type)) return
  form.fields.unshift(defaultField(type))
  quickType.value = ''
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

  if (
    !f.label ||
    f.label.trim() === '' ||
    FIELD_TYPES.some(t => t.label === f.label)
  ) {
    f.label = meta.label
  }

  if (!f.value && meta.prefix) {
    f.value = meta.prefix
  }
}

const normalizeValue = (f) => {
  const v = (f.value || '').trim()
  const meta = getFieldMeta(f?.type)

  if (v && meta.urlLike) {
    f.value = /^https?:\/\//i.test(v) ? v : `https://${v}`
  } else {
    f.value = v
  }
}

const { $toast } = useNuxtApp() // or useToast if auto-imported, checking imports
// Actually, looking at previous grep, useToast is likely a composable.
// Let's check imports in the file.
// The file uses <script setup>, so auto-imports might be available.
// The plan said "Import useToast".
// Let's check if useToast is auto-imported or needs explicit import.
// Usually in Nuxt 3 it's auto-imported.
// I will assume auto-import for now, but if not I'll add it.
// Wait, I should check if I need to add `const toast = useToast()`
// The grep showed `composables/useToast.js`.
// So `const toast = useToast()` should work.

const toast = useToast()
const { $api } = useApi()
const config = useRuntimeConfig()

const resolveAvatar = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${config.public.apiBase}${url}`
}

const hasCustomAvatar = computed(() => {
  const url = form.avatar_url || ''
  // Se non inizia con http (quindi è relativo /static/...) è custom
  // Oppure se è un URL assoluto ma non è dicebear
  return url && !url.includes('dicebear.com')
})

const onFileSelect = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  const fd = new FormData()
  fd.append('file', file)
  
  try {
    const res = await $api(`/cards/${props.cardId}/avatar`, {
      method: 'POST',
      body: fd
    })
    // Update form avatar
    form.avatar_url = res.avatar_url
    toast.success('Avatar updated!')
  } catch (e) {
    // Error handled by useApi usually
  }
}

const deleteAvatar = async () => {
  if (!confirm('Do you want to remove the custom avatar?')) return
  
  try {
    const res = await $api(`/cards/${props.cardId}/avatar`, {
      method: 'DELETE'
    })
    form.avatar_url = res.avatar_url
    toast.success('Avatar removed.')
  } catch (e) {
    // Error handled by useApi
  }
}

const onSubmit = () => {
  // Validation: check for empty fields
  const hasEmptyFields = form.fields.some(f => !f.value || !f.value.trim())
  if (hasEmptyFields) {
    toast.error('Fill in all added fields or remove them.')
    return
  }

  const cleaned = {
    title: (form.title || '').trim(),
    slug: (form.slug || '').trim(),
    notes: (form.bio || '').trim(),
    theme: (form.theme || 'minimal'),
    avatar_url: form.avatar_url,
    is_public: !!form.is_public,
    is_indexed: !!form.is_indexed,
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

const upgradeToPro = async () => {
  try {
    const res = await $api('/payment/checkout', { method: 'POST' })
    if (res.url) {
      window.location.href = res.url
    }
  } catch (e) {
    console.error(e)
    if (e.message.includes('Stripe not configured')) {
        toast.error("Stripe keys missing in Admin Settings")
    } else {
        toast.error("Error starting checkout")
    }
  }
}
</script>
