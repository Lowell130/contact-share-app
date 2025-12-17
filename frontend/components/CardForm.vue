<template>
  <div class="max-w-[1600px] mx-auto">
    <!-- Main Grid Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- LEFT COLUMN: EDITOR -->
      <div class="lg:col-span-7 space-y-8">
        <form @submit.prevent="onSubmit" id="card-form" class="space-y-8 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          
          <!-- Header & Actions -->
          <div class="flex items-center justify-between border-b border-gray-100 pb-4">
             <div>
                <h2 class="text-xl font-bold text-gray-900">Card Editor</h2>
                <p class="text-sm text-gray-500">Customize your digital business card</p>
             </div>
             <!-- Save Button (Desktop) -->
             <button
                type="submit"
                class="hidden lg:flex items-center gap-2 bg-black text-white px-6 py-2.5 rounded-full font-medium hover:bg-gray-800 transition-colors shadow-lg shadow-gray-200/50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Save Changes</span>
              </button>
          </div>

          <!-- Avatar Section -->
          <section>
             <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Profile Image</h3>
             <div class="flex items-center gap-6">
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
                  <p v-if="!cardId" class="text-sm text-gray-500">
                    Save the card first to upload a custom avatar.
                  </p>
                  <div v-else>
                    <p class="text-sm text-gray-500 mb-2">
                       Upload a professional photo or logo.<br>Square format (JPG, PNG).
                    </p>
                    <button 
                      v-if="hasCustomAvatar"
                      type="button"
                      @click="deleteAvatar"
                      class="text-xs text-red-600 hover:text-red-800 font-medium flex items-center gap-1"
                    >
                      Remove custom avatar
                    </button>
                  </div>
                </div>
             </div>
          </section>

          <!-- Basic Info -->
          <section class="grid grid-cols-1 md:grid-cols-2 gap-5">
             <div class="col-span-full">
                <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Basic Info</h3>
             </div>
             
             <div>
               <label class="block mb-2 text-sm font-medium text-gray-700">Display Name</label>
               <input
                 v-model="form.title"
                 class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm py-2.5 px-3"
                 placeholder="e.g. Alex Smith"
                 required
               />
             </div>
             
             <div>
               <label class="block mb-2 text-sm font-medium text-gray-700">
                 Slug (URL)
                 <span class="text-gray-400 font-normal text-xs ml-1">getcontact.share/c/<strong>slug</strong></span>
               </label>
               <input
                 v-model="form.slug"
                 class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm py-2.5 px-3"
                 placeholder="alex-smith"
               />
             </div>

             <div class="col-span-full">
                <label class="block mb-2 text-sm font-medium text-gray-700">Bio / Headline</label>
                <textarea
                  v-model="form.bio"
                  rows="3"
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-3"
                  placeholder="Senior Product Designer at TechCorp..."
                />
             </div>
          </section>

          <!-- Theme Selection -->
          <section>
             <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Visual Theme</h3>
             
             <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
                <button
                   v-for="t in availableThemes"
                   :key="t.id"
                   type="button"
                   @click="selectTheme(t)"
                   :class="[
                      'relative w-full aspect-square rounded-xl border-2 transition-all overflow-hidden flex flex-col items-center justify-center gap-1 group',
                      form.theme === t.id ? 'border-blue-600 shadow-md scale-105' : 'border-transparent hover:border-gray-200 bg-gray-50'
                   ]"
                >
                   <!-- Color Preview -->
                   <div :class="['w-8 h-8 rounded-full shadow-sm', t.class]"></div>
                   <span class="text-[10px] font-medium text-gray-600 truncate w-full text-center px-1">{{ t.name }}</span>
                   
                   <!-- Validation Badge -->
                   <div v-if="t.locked" class="absolute inset-0 bg-white/60 flex items-center justify-center backdrop-blur-[1px]">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                         <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                      </svg>
                   </div>
                </button>
             </div>
             
             <div v-if="!isPro" class="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100 flex items-center justify-between">
                <div class="flex items-center gap-3">
                   <div class="p-2 bg-blue-100 rounded-full text-blue-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                   </div>
                   <div>
                       <p class="text-sm font-bold text-blue-900">Unlock Pro Themes</p>
                       <p class="text-xs text-blue-700">Get access to all premium styles.</p>
                   </div>
                </div>
                <button type="button" @click="upgradeToPro" class="text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full transition-colors">
                   Upgrade
                </button>
             </div>
          </section>

          <!-- Contact Fields -->
          <section>
             <div class="flex items-center justify-between mb-4">
                <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider">Contact Fields</h3>
             </div>

             <!-- Field List -->
             <div class="space-y-3 mb-6">
                <!-- Empty State -->
                <div v-if="!form.fields.length" class="text-center py-8 border-2 border-dashed border-gray-200 rounded-xl">
                   <p class="text-sm text-gray-500">You haven't added any fields yet.</p>
                   <p class="text-xs text-gray-400 mt-1">Start by adding your Email or Social links below.</p>
                </div>

                <div 
                   v-for="(f, i) in form.fields" 
                   :key="i"
                   draggable="true"
                   @dragstart="onDragStart(i, $event)"
                   @dragover.prevent
                   @dragenter.prevent
                   @drop="onDrop(i)"
                   @dragend="onDragEnd"
                   :class="{'opacity-50 ring-2 ring-blue-500': dragIndex === i}"
                   class="group bg-white border border-gray-200 rounded-lg p-3 shadow-sm hover:border-blue-300 transition-all flex items-start gap-3 cursor-grab active:cursor-grabbing"
                >
                   <!-- Icon / Drag Handle -->
                   <div class="mt-2.5 text-gray-400 cursor-move">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
                      </svg>
                   </div>
                   
                   <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
                      <!-- Input Group -->
                      <div class="space-y-1">
                         <label class="text-[10px] uppercase text-gray-500 font-bold tracking-wider">Label</label>
                         <input v-model="f.label" class="block w-full text-sm border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 py-2 px-3" :placeholder="placeholderFor(f).label" />
                      </div>
                      <div class="space-y-1">
                         <label class="text-[10px] uppercase text-gray-500 font-bold tracking-wider">Value</label>
                         <input 
                            v-model="f.value" 
                            @blur="normalizeValue(f)"
                            class="block w-full text-sm border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 py-2 px-3" 
                            :placeholder="placeholderFor(f).value" 
                         />
                      </div>
                   </div>

                   <!-- Actions -->
                   <div class="flex flex-col gap-2 mt-1">
                      <button type="button" @click="removeField(i)" class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors">
                         <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                         </svg>
                      </button>
                      <label class="cursor-pointer p-1.5 text-gray-400 hover:text-blue-600 rounded-md" :title="f.visible ? 'Hide field' : 'Show field'">
                         <input type="checkbox" v-model="f.visible" class="hidden" />
                         <svg v-if="f.visible" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                         </svg>
                         <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                         </svg>
                      </label>
                   </div>
                </div>
             </div>

             <!-- Add Field Bar -->
             <div class="bg-gray-50 border border-gray-200 rounded-xl p-3 flex flex-wrap items-center gap-2">
                <select v-model="quickType" class="bg-white border-gray-300 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 min-w-[150px]">
                   <option disabled value="">Select field type</option>
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
                  class="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm px-5 py-2.5 flex items-center gap-2 transition-colors"
                >
                   <span>+ Add Field</span>
                </button>
             </div>
          </section>

          <!-- Settings -->
          <section class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50 p-4 rounded-xl border border-gray-100">
             <div>
                <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">Visibility</h3>
                <div class="space-y-2">
                   <label class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:border-blue-300">
                      <input type="radio" v-model="visibilityMode" value="public_indexed" class="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                      <div>
                         <span class="block text-sm font-medium text-gray-900">Public & Indexed</span>
                         <span class="block text-xs text-gray-500">Visible to everyone and search engines</span>
                      </div>
                   </label>
                   <label class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:border-blue-300">
                      <input type="radio" v-model="visibilityMode" value="public_noindex" class="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                      <div>
                         <span class="block text-sm font-medium text-gray-900">Public (No Index)</span>
                         <span class="block text-xs text-gray-500">Accessible via link, hidden from Google</span>
                      </div>
                   </label>
                   <label class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:border-blue-300">
                      <input type="radio" v-model="visibilityMode" value="private" class="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                      <div>
                         <span class="block text-sm font-medium text-gray-900">Private</span>
                         <span class="block text-xs text-gray-500">Only you can see this card</span>
                      </div>
                   </label>
                </div>
             </div>

             <div>
                <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">Options</h3>
                <label class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:border-blue-300">
                   <input type="checkbox" v-model="form.allow_vcard" class="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                   <div>
                       <span class="block text-sm font-medium text-gray-900">Allow vCard Download</span>
                       <span class="block text-xs text-gray-500">Visitors can save your contact to their phone</span>
                   </div>
                </label>
             </div>
          </section>

          <!-- Mobile Save Button -->
          <div class="lg:hidden sticky bottom-4 z-20">
             <button
                type="submit"
                class="w-full flex justify-center items-center gap-2 bg-black text-white px-6 py-4 rounded-xl font-bold shadow-xl"
              >
                <span>Save Changes</span>
              </button>
          </div>

        </form>
      </div>

      <!-- RIGHT COLUMN: LIVE PREVIEW -->
      <div class="hidden lg:flex lg:col-span-5 sticky top-8 h-[calc(100vh-4rem)] bg-gray-50 rounded-xl border border-gray-200 p-8 items-center justify-center">
         
         <!-- Minimal Device Simulator -->
         <div class="w-[375px] h-[667px] max-w-full max-h-full bg-white shadow-2xl rounded-[2rem] overflow-hidden border-8 border-gray-800 flex flex-col relative shrink-0 mx-auto">
            
            <!-- Minimal Header/Status Bar indicator -->
            <div class="h-6 w-full bg-white border-b border-gray-100 absolute top-0 z-10 flex items-center justify-center">
                 <div class="w-20 h-4 bg-gray-100 rounded-b-lg"></div>
            </div>

            <!-- Screen Content (Iframe) -->
            <div class="flex-1 bg-white relative w-full h-full pt-6"> <!-- pt-6 to clear header -->
               <iframe 
                  ref="previewFrame"
                  src="/cards/preview-frame"
                  class="w-full h-full border-0"
                  title="Mobile Preview"
                  @load="onFrameLoad"
               ></iframe>
            </div>
         </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, computed, onMounted } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  cardId: { type: String, default: null }
})
const emit = defineEmits(['update:modelValue', 'submit'])

// === DEPENDENCIES ===
const { user } = useAuth()
const { $api } = useApi()
const toast = useToast()
const config = useRuntimeConfig()
const mounted = ref(false)

// onMounted merged below with message listener

const isPro = computed(() => user.value?.plan === 'pro' || user.value?.plan === 'admin')

// === FORM STATE ===
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

// === DRAG & DROP ===
const dragIndex = ref(null)

const onDragStart = (index, event) => {
    dragIndex.value = index
    event.dataTransfer.effectAllowed = 'move'
    // Optional: set drag image ghost if needed
}

const onDrop = (index) => {
    const fromIndex = dragIndex.value
    if (fromIndex === null || fromIndex === index) return
    
    // Move item in array
    const item = form.fields.splice(fromIndex, 1)[0]
    form.fields.splice(index, 0, item)
    dragIndex.value = null
}

const onDragEnd = () => {
    dragIndex.value = null
}


// === PREVIEW IFRAME LOGIC ===
const previewFrame = ref(null)
const frameReady = ref(false)

const previewPayload = computed(() => ({
  ...form,
  id: props.cardId || 'preview',
  slug: form.slug || 'your-slug',
  notes: form.bio, // map bio back to notes
  fields: form.fields
}))

const sendPreviewUpdate = () => {
    if (!previewFrame.value?.contentWindow) return
    previewFrame.value.contentWindow.postMessage({
        type: 'PREVIEW_UPDATE',
        payload: JSON.parse(JSON.stringify(previewPayload.value))
    }, '*')
}

// Handle message from iframe (e.g. "PREVIEW_READY")
const onMessage = (event) => {
    if (event.data && event.data.type === 'PREVIEW_READY') {
        frameReady.value = true
        sendPreviewUpdate()
    }
}

onMounted(() => { 
    mounted.value = true 
    window.addEventListener('message', onMessage)
})

onUnmounted(() => {
    window.removeEventListener('message', onMessage)
})

const onFrameLoad = () => {
    // Fallback if message isn't received
    frameReady.value = true
    sendPreviewUpdate()
}

// Watch changes and send to iframe
watch(previewPayload, () => {
    sendPreviewUpdate()
}, { deep: true })


// === THEMES ===
const availableThemes = [
    { id: 'minimal', name: 'Minimal', class: 'bg-white border-gray-200' },
    { id: 'gradient', name: 'Gradient', class: 'bg-gradient-to-br from-pink-500 to-orange-400' },
    { id: 'dark', name: 'Dark Mode', class: 'bg-gray-900' },
    { id: 'flowbite', name: 'Forest', class: 'bg-green-50' },
    { id: 'modern_emerald', name: 'Emerald', class: 'bg-emerald-500', locked: true },
    { id: 'modern_blue', name: 'Blue', class: 'bg-blue-600', locked: true },
    { id: 'modern_indigo', name: 'Indigo', class: 'bg-indigo-600', locked: true },
    { id: 'modern_rose', name: 'Rose', class: 'bg-rose-500', locked: true },
    { id: 'modern_orange', name: 'Orange', class: 'bg-orange-500', locked: true },
].map(t => ({ ...t, locked: t.locked && !isPro.value }))

const selectTheme = (t) => {
    if (t.locked) {
        toast.info("This theme requires a Pro plan.")
        return
    }
    form.theme = t.id
}

// === FIELD CONFIG ===
const FIELD_CONFIG = {
  email: { label: 'Email', placeholder: 'name@example.com', urlLike: false },
  mobile: { label: 'Mobile', placeholder: '+1 234 567 890', urlLike: false },
  phone: { label: 'Phone', placeholder: '+1 234 567 890', urlLike: false },
  url: { label: 'Website', placeholder: 'https://example.com', urlLike: true },
  linkedin: { label: 'LinkedIn', placeholder: 'linkedin.com/in/you', urlLike: true, prefix: 'https://linkedin.com/in/' },
  instagram: { label: 'Instagram', placeholder: 'instagram.com/you', urlLike: true, prefix: 'https://instagram.com/' },
  x: { label: 'X (Twitter)', placeholder: 'x.com/you', urlLike: true, prefix: 'https://x.com/' },
  facebook: { label: 'Facebook', placeholder: 'facebook.com/you', urlLike: true, prefix: 'https://facebook.com/' },
  whatsapp: { label: 'WhatsApp', placeholder: 'wa.me/1234567', urlLike: true, prefix: 'https://wa.me/' },
  telegram: { label: 'Telegram', placeholder: 't.me/username', urlLike: true, prefix: 'https://t.me/' },
  github: { label: 'GitHub', placeholder: 'github.com/you', urlLike: true, prefix: 'https://github.com/' },
  youtube: { label: 'YouTube', placeholder: 'youtube.com/@channel', urlLike: true, prefix: 'https://youtube.com/@' },
  tiktok: { label: 'TikTok', placeholder: 'tiktok.com/@user', urlLike: true, prefix: 'https://tiktok.com/@' },
  twitch: { label: 'Twitch', placeholder: 'twitch.tv/user', urlLike: true, prefix: 'https://twitch.tv/' },
  strava: { label: 'Strava', placeholder: 'strava.com/athletes/123', urlLike: true, prefix: 'https://strava.com/athletes/' },
  onlyfans: { label: 'OnlyFans', placeholder: 'onlyfans.com/u123', urlLike: true, prefix: 'https://onlyfans.com/' },
  company: { label: 'Company', placeholder: 'Acme Inc.', urlLike: false },
  role: { label: 'Role', placeholder: 'Product Manager', urlLike: false },
  address: { label: 'Address', placeholder: '123 Main St, City', urlLike: false },
  note: { label: 'Note', placeholder: 'Custom text...', urlLike: false }
}

const FIELD_TYPES = Object.entries(FIELD_CONFIG).map(([value, meta]) => ({
  value,
  label: meta.label
}))

function getFieldMeta(type) {
    const key = String(type || '').toLowerCase()
    return FIELD_CONFIG[key] || FIELD_CONFIG.email
}

const quickType = ref('email')

const addField = (type) => {
  if (!type) return
  if (form.fields.some(f => f.type === type)) {
      toast.info("You already have this field.")
      return
  }
  const meta = getFieldMeta(type)
  form.fields.push({
    type,
    label: meta.label,
    value: meta.prefix || '',
    visible: true
  })
  quickType.value = ''
}

const removeField = (i) => {
  form.fields.splice(i, 1)
}

const placeholderFor = (f) => getFieldMeta(f?.type)

const normalizeValue = (f) => {
  const v = (f.value || '').trim()
  const meta = getFieldMeta(f?.type)
  if (v && meta.urlLike) {
    // Basic fix
    if (!/^https?:\/\//i.test(v)) {
        f.value = `https://${v}`
    }
  }
}

// === VISIBILITY ===
const visibilityMode = computed({
  get() {
    if (!form.is_public) return 'private'
    return form.is_indexed ? 'public_indexed' : 'public_noindex'
  },
  set(val) {
    if (val === 'private') {
      form.is_public = false
      form.is_indexed = false
    } else if (val === 'public_noindex') {
      form.is_public = true
      form.is_indexed = false
    } else {
      form.is_public = true
      form.is_indexed = true
    }
  }
})

// === AVATAR LOGIC ===
const resolveAvatar = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${config.public.apiBase}${url}`
}

const hasCustomAvatar = computed(() => {
  const url = form.avatar_url || ''
  return url && !url.includes('dicebear.com')
})

const onFileSelect = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  if (!props.cardId) {
      toast.error('Please save the card created first.')
      return
  }
  
  const fd = new FormData()
  fd.append('file', file)
  
  try {
    const res = await $api(`/cards/${props.cardId}/avatar`, {
      method: 'POST',
      body: fd
    })
    form.avatar_url = res.avatar_url
    toast.success('Avatar updated!')
  } catch (e) {
    console.error(e)
  }
}

const deleteAvatar = async () => {
    if (!confirm('Remove custom avatar?')) return
    try {
        await $api(`/cards/${props.cardId}/avatar`, { method: 'DELETE' })
        form.avatar_url = ''
        toast.success('Avatar removed.')
    } catch (e) {}
}

const upgradeToPro = async () => {
    try {
        const res = await $api('/payment/checkout', { method: 'POST' })
        if (res.url) window.location.href = res.url
    } catch (e) {
        toast.error("Could not start checkout.")
    }
}

// === SUBMIT ===
watch(form, () => emit('update:modelValue', form), { deep: true })

const onSubmit = () => {
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
      .filter(x => x.type && x.value) 
  }
  emit('submit', cleaned)
}
</script>
