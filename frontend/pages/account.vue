<template>
  <section class="max-w-2xl mx-auto py-10 px-4">
    <h1 class="text-3xl font-bold mb-8">Account Settings</h1>
    
    <!-- Subscription Section for PRO users -->
    <div v-if="user?.plan === 'pro'" class="bg-white shadow rounded-lg p-6 border border-gray-200 mb-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Subscription</h2>
      
      <div class="flex items-center justify-between mb-4">
        <div>
          <p class="text-sm text-gray-600">Current Plan</p>
          <p class="text-lg font-medium text-gray-900">Pro - €4.99/month</p>
        </div>
        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
          Active
        </span>
      </div>
      
      <button
        @click="manageSubscription"
        :disabled="loading"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ loading ? 'Loading...' : 'Manage Subscription' }}
      </button>
      
      <p class="mt-3 text-xs text-gray-500 text-center">
        Cancel anytime, update payment method, or view invoices via Stripe
      </p>
    </div>
    
    <!-- Free Plan CTA -->
    <div v-else class="bg-white shadow rounded-lg p-6 border border-gray-200 mb-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Subscription</h2>
      <p class="text-gray-600 mb-4">You're currently on the Free plan.</p>
      <NuxtLink 
        to="/upgrade"
        class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
      >
        Upgrade to Pro
      </NuxtLink>
    </div>
    
    <!-- Danger Zone -->
    <div class="bg-white shadow rounded-lg p-6 border border-gray-200">
      <h2 class="text-xl font-semibold text-red-600 mb-4">Danger Zone</h2>
      <p class="text-gray-600 mb-6">
        Deleting your account is irreversible. All your cards, data, and statistics will be permanently removed.
      </p>
      
      <button
        @click="deleteAccount"
        class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
      >
        Delete Account
      </button>
    </div>
  </section>
</template>

<script setup>
const { $api } = useApi()
const { logout, user, refreshUser } = useAuth()
const router = useRouter()
const toast = useToast()

const loading = ref(false)

// Refresh user data when returning from Stripe portal
onMounted(async () => {
  await refreshUser()
})

const manageSubscription = async () => {
  loading.value = true
  try {
    const res = await $api('/payment/portal', { method: 'POST' })
    if (res.url) {
      window.location.href = res.url
    }
  } catch (e) {
    console.error(e)
    toast.error('Error opening subscription portal')
  } finally {
    loading.value = false
  }
}

const deleteAccount = async () => {
  if (!confirm('Are you sure you want to delete your account? This action is IRREVERSIBLE.')) return
  if (!confirm('Do you really confirm? All your data will be lost forever.')) return

  try {
    await $api('/auth/me', { method: 'DELETE' })
    toast.success('Account deleted successfully.')
    await logout()
    router.push('/')
  } catch (e) {
    toast.error('Error deleting account.')
    console.error(e)
  }
}
</script>
