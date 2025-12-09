<template>
  <section class="max-w-2xl mx-auto py-10 px-4">
    <h1 class="text-3xl font-bold mb-8">Account Settings</h1>
    
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 border border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-semibold text-red-600 mb-4">Danger Zone</h2>
      <p class="text-gray-600 dark:text-gray-300 mb-6">
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
const { logout } = useAuth()
const router = useRouter()
const { success, error } = useToast()

const deleteAccount = async () => {
  if (!confirm('Are you sure you want to delete your account? This action is IRREVERSIBLE.')) return
  if (!confirm('Do you really confirm? All your data will be lost forever.')) return

  try {
    await $api('/auth/me', { method: 'DELETE' })
    success('Account deleted successfully.')
    await logout()
    router.push('/')
  } catch (e) {
    error('Error deleting account.')
    console.error(e)
  }
}
</script>
