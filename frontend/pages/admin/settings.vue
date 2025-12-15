<template>
  <div class="bg-white shadow rounded-lg p-6 max-w-2xl">
    <h3 class="text-lg font-medium text-gray-900 mb-6">System Settings</h3>
    
    <form @submit.prevent="save" class="space-y-6">
        <div>
            <label class="block text-sm font-medium text-gray-700">Stripe Secret Key (SK)</label>
            <input v-model="form.stripe_secret_key" type="password" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        
        <div>
            <label class="block text-sm font-medium text-gray-700">Stripe Webhook Secret (WHSEC)</label>
            <input v-model="form.stripe_webhook_secret" type="password" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        
        <div>
            <label class="block text-sm font-medium text-gray-700">Stripe Price ID (price_...)</label>
            <input v-model="form.stripe_price_id" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
            <p class="mt-1 text-xs text-gray-500">ID of the recurring price created in Stripe Dashboard.</p>
        </div>
        
        <div class="flex justify-end">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save Settings</button>
        </div>
    </form>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin', middleware: 'admin' })
const { $api } = useApi()
const toast = useToast()

const form = reactive({
    stripe_secret_key: '',
    stripe_webhook_secret: '',
    stripe_price_id: ''
})

onMounted(async () => {
    try {
        const data = await $api('/admin/settings')
        if(data) Object.assign(form, data)
    } catch(e) {
        console.error(e)
    }
})

async function save() {
    try {
        await $api('/admin/settings', {
            method: 'PUT',
            body: form
        })
        toast.success("Settings saved")
    } catch(e) {
        toast.error("Error saving settings")
    }
}
</script>
