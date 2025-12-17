<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Set New Password
        </h2>
      </div>
      
      <form v-if="!success" class="mt-8 space-y-6" @submit.prevent="onSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="password" class="sr-only">New Password</label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              v-model="password"
              required 
              minlength="6"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="New Password" 
            />
          </div>
          <div>
             <label for="confirm" class="sr-only">Confirm Password</label>
             <input 
               id="confirm" 
               name="confirm" 
               type="password" 
               v-model="confirm"
               required 
               minlength="6"
               class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
               placeholder="Confirm New Password" 
             />
           </div>
        </div>

        <div v-if="error" class="text-sm text-red-500 text-center font-medium">
            {{ error }}
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ loading ? 'Updating...' : 'Update Password' }}
          </button>
        </div>
      </form>
      
      <div v-else class="mt-8 text-center">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <h3 class="mt-2 text-xl font-medium text-gray-900">Success!</h3>
        <p class="mt-2 text-sm text-gray-500">
            Your password has been updated properly.
        </p>
        <div class="mt-4">
            <NuxtLink to="/login" class="text-sm font-medium text-blue-600 hover:text-blue-500">Login now</NuxtLink>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const route = useRoute()
const router = useRouter()
const { $api } = useApi()

const password = ref('')
const confirm = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

const onSubmit = async () => {
    error.value = ''
    if (password.value !== confirm.value) {
        error.value = 'Passwords do not match'
        return
    }
    
    // Check for token
    const token = route.query.token
    if (!token) {
        error.value = 'Missing or invalid token'
        return
    }

    loading.value = true
    try {
        await $api('/auth/reset-password', {
            method: 'POST',
            body: { token, new_password: password.value }
        })
        success.value = true
    } catch (e) {
        console.error(e)
        const msg = e.response?._data?.detail || 'Failed to reset password (token might be expired)'
        error.value = msg
    } finally {
        loading.value = false
    }
}
</script>
