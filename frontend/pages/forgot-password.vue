<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Reset Password
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Enter your email and we'll send you a link to reset your password.
        </p>
      </div>
      <form v-if="!submitted" class="mt-8 space-y-6" @submit.prevent="onSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input 
              id="email-address" 
              name="email" 
              type="email" 
              v-model="email"
              required 
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Email address" 
            />
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ loading ? 'Sending...' : 'Send Reset Link' }}
          </button>
        </div>
        
        <div v-if="error" class="text-center text-sm text-red-500 font-medium">
            {{ error }}
        </div>
      </form>
      
      <div v-else class="mt-8 text-center">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <h3 class="mt-2 text-xl font-medium text-gray-900">Check your inbox</h3>
        <p class="mt-2 text-sm text-gray-500">
            We sent a password reset link to {{ email }}.
        </p>
        <div class="mt-4">
            <NuxtLink to="/login" class="text-sm font-medium text-blue-600 hover:text-blue-500">Back to login</NuxtLink>
        </div>
      </div>
    
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const { $api } = useApi()
const email = ref('')
const loading = ref(false)
const submitted = ref(false)
const error = ref('')

const onSubmit = async () => {
    loading.value = true
    error.value = ''
    try {
        await $api('/auth/forgot-password', {
            method: 'POST',
            body: { email: email.value }
        })
        submitted.value = true
    } catch (e) {
        // We generally don't want to reveal if email failed due to logic, 
        // but unexpected errors might happen
        console.error(e)
        // For security we might still show submitted, but let's show generic error if something breaks hard
        error.value = 'Something went wrong. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>
