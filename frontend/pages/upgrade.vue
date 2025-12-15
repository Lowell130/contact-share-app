<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-extrabold text-gray-900">Upgrade to Pro</h2>
        <p class="mt-4 text-xl text-gray-500">Unlock the full power of ContactShare.</p>
      </div>

      <div class="space-y-12 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-8 max-w-4xl mx-auto">
          <!-- Free Tier -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col hover:shadow-lg transition-shadow opacity-75">
            <div class="mb-4">
              <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                Current Plan
              </span>
            </div>
            <h3 class="text-4xl font-extrabold text-gray-900">Free</h3>
            <p class="mt-4 text-gray-500">Basic features.</p>
            <ul class="mt-6 space-y-4 flex-1">
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">1 Digital Card</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Basic Themes</span>
              </li>
            </ul>
             <button disabled class="mt-8 block w-full bg-gray-100 border border-gray-200 rounded-md py-3 text-sm font-semibold text-gray-500 text-center cursor-not-allowed">
               Active
             </button>
          </div>

          <!-- Pro Tier -->
          <div class="bg-white rounded-2xl shadow-xl border-2 border-blue-600 p-8 flex flex-col relative overflow-hidden transform scale-105">
             <div class="absolute top-0 right-0 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">
                 Recommended
             </div>
            <div class="mb-4">
              <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                Pro
              </span>
            </div>
            <h3 class="text-4xl font-extrabold text-gray-900">
                €4.99<span class="text-xl font-medium text-gray-500">/mo</span>
            </h3>
            <p class="mt-4 text-gray-500">For serious networking.</p>
            <ul class="mt-6 space-y-4 flex-1">
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-900 font-medium">Unlimited Cards</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-900 font-medium">Exclusive Premium Themes</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-900 font-medium">Advanced Analytics</span>
              </li>
            </ul>
             <button @click="upgradeToPro" class="mt-8 block w-full bg-blue-600 border border-transparent rounded-md py-3 text-sm font-semibold text-white text-center hover:bg-blue-700 shadow-md transition-all">
               Upgrade Now using Stripe
             </button>
          </div>
        </div>

        <div class="mt-12 text-center">
            <NuxtLink to="/dashboard" class="text-blue-600 hover:underline">
                &larr; Back to Dashboard
            </NuxtLink>
        </div>
    </div>
  </div>
</template>

<script setup>
const { $api } = useApi()
const toast = useToast()

const upgradeToPro = async () => {
  try {
    const res = await $api('/payment/checkout', { method: 'POST' })
    if (res.url) {
      window.location.href = res.url
    }
  } catch (e) {
    console.error(e)
    if (e.message.includes('Stripe not configured')) {
        toast.error("Stripe not configured. Please contact support.")
    } else {
        toast.error("Error initiating checkout.")
    }
  }
}
</script>
