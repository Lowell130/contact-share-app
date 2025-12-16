<template>
  <div class="bg-white">
    <!-- Hero Section -->
    <section class="relative overflow-hidden pt-16 pb-20 lg:pt-24 lg:pb-28">
      <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block xl:inline">Your business card,</span>
            <span class="block text-blue-600 xl:inline">reinvented.</span>
          </h1>
          <p class="mx-auto mt-3 max-w-md text-base text-gray-500 sm:text-lg md:mt-5 md:max-w-3xl md:text-xl">
            Create, customize, and share your professional identity in seconds. 
            Sustainable, smart, and always up-to-date. Make an impact at first sight.
          </p>
          
          <div class="mt-10 max-w-sm mx-auto sm:max-w-none sm:flex sm:justify-center gap-4">
            <div v-if="!isLoggedIn" class="space-y-4 sm:space-y-0 sm:flex sm:gap-4">
              <NuxtLink
                to="/register"
                class="flex items-center justify-center rounded-full border border-transparent bg-blue-600 px-8 py-3 text-base font-medium text-white hover:bg-blue-700 md:py-4 md:px-10 md:text-lg shadow-lg hover:shadow-xl transition-all"
              >
                Start for Free
              </NuxtLink>
              <NuxtLink
                to="/login"
                class="flex items-center justify-center rounded-full border border-gray-300 bg-white px-8 py-3 text-base font-medium text-gray-700 hover:bg-gray-50 md:py-4 md:px-10 md:text-lg"
              >
                Login
              </NuxtLink>
            </div>
            <div v-else>
              <NuxtLink
                to="/dashboard"
                class="flex items-center justify-center rounded-full border border-transparent bg-blue-600 px-8 py-3 text-base font-medium text-white hover:bg-blue-700 md:py-4 md:px-10 md:text-lg shadow-lg"
              >
                Go to Dashboard
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Decorative Blob -->
      <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -z-10 opacity-30 blur-3xl pointer-events-none">
        <div class="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc]" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"></div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-gray-50 overflow-hidden lg:py-24">
      <div class="relative max-w-xl mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl">
        <div class="relative">
          <h2 class="text-center text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Why choose ContactShare?
          </h2>
          <p class="mt-4 max-w-3xl mx-auto text-center text-xl text-gray-500">
            Everything you need to manage your contacts professionally and efficiently.
          </p>
        </div>

        <div class="relative mt-12 lg:mt-24 lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
          <div class="relative">
            <h3 class="text-2xl font-extrabold text-gray-900 tracking-tight sm:text-3xl">
              Digital & Sustainable
            </h3>
            <p class="mt-3 text-lg text-gray-500">
              Forget paper business cards that end up in the trash. Your digital card is always with you, on your smartphone, ready to be shared. Reduce waste and make an eco-friendly choice.
            </p>

            <dl class="mt-10 space-y-10">
              <div class="relative">
                <dt>
                  <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                    </svg>
                  </div>
                  <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Instant Sharing</p>
                </dt>
                <dd class="mt-2 ml-16 text-base text-gray-500">
                  Share via QR Code, Direct Link, Email, or WhatsApp. Recipients don't need to install anything.
                </dd>
              </div>

              <div class="relative">
                <dt>
                  <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Integrated Analytics</p>
                </dt>
                <dd class="mt-2 ml-16 text-base text-gray-500">
                  Discover how many people visit your card and download your contacts. Optimize your presence.
                </dd>
              </div>
            </dl>
          </div>

          <div class="mt-10 -mx-4 relative lg:mt-0" aria-hidden="true">
             <!-- Placeholder for Feature Image -->
             <div class="relative mx-auto w-[22rem] rounded-3xl shadow-2xl border-8 border-gray-900 bg-white overflow-hidden h-[40rem] flex flex-col">
                <!-- Mockup Header -->
                <div class="h-32 bg-gradient-to-br from-blue-500 to-purple-600 w-full"></div>
                <div class="px-6 -mt-12">
                   <div class="w-24 h-24 rounded-full border-4 border-white bg-gray-200 mx-auto overflow-hidden">
                      <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="Avatar" class="w-full h-full object-cover" />
                   </div>
                   <div class="text-center mt-4 space-y-1">
                      <div class="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
                      <div class="h-3 bg-gray-100 rounded w-1/2 mx-auto"></div>
                   </div>
                   <div class="mt-8 space-y-4">
                      <div class="h-12 bg-gray-50 rounded-xl border border-gray-100 flex items-center px-4 gap-3">
                         <div class="w-8 h-8 rounded-full bg-blue-100"></div>
                         <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                      </div>
                      <div class="h-12 bg-gray-50 rounded-xl border border-gray-100 flex items-center px-4 gap-3">
                         <div class="w-8 h-8 rounded-full bg-green-100"></div>
                         <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                      </div>
                      <div class="h-12 bg-gray-50 rounded-xl border border-gray-100 flex items-center px-4 gap-3">
                         <div class="w-8 h-8 rounded-full bg-purple-100"></div>
                         <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-extrabold text-gray-900">How it works</h2>
          <p class="mt-4 text-lg text-gray-500">Get started in three simple steps.</p>
        </div>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div class="text-center">
            <div class="flex items-center justify-center h-16 w-16 rounded-full bg-blue-100 text-blue-600 mx-auto mb-4 text-2xl font-bold">1</div>
            <h3 class="text-xl font-medium text-gray-900">Create Account</h3>
            <p class="mt-2 text-gray-500">Sign up for free in seconds.</p>
          </div>
          <div class="text-center">
            <div class="flex items-center justify-center h-16 w-16 rounded-full bg-blue-100 text-blue-600 mx-auto mb-4 text-2xl font-bold">2</div>
            <h3 class="text-xl font-medium text-gray-900">Customize</h3>
            <p class="mt-2 text-gray-500">Add photos, details, and social links.</p>
          </div>
          <div class="text-center">
            <div class="flex items-center justify-center h-16 w-16 rounded-full bg-blue-100 text-blue-600 mx-auto mb-4 text-2xl font-bold">3</div>
            <h3 class="text-xl font-medium text-gray-900">Share</h3>
            <p class="mt-2 text-gray-500">Show your QR or send the link to anyone.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-extrabold text-gray-900">Simple, transparent pricing</h2>
          <p class="mt-4 text-lg text-gray-500">Choose the plan that fits your needs.</p>
        </div>
        
        <div class="space-y-12 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-8 max-w-4xl mx-auto">
          <!-- Free Tier -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col hover:shadow-lg transition-shadow">
            <div class="mb-4">
              <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                Starter
              </span>
            </div>
            <h3 class="text-4xl font-extrabold text-gray-900">Free</h3>
            <p class="mt-4 text-gray-500">Everything you need to get started.</p>
            <ul class="mt-6 space-y-4 flex-1">
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">1 Digital Card</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Basic Themes</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Unlimited Sharing</span>
              </li>
            </ul>
             <NuxtLink v-if="!isLoggedIn" to="/register" class="mt-8 block w-full bg-gray-50 border border-gray-200 rounded-md py-3 text-sm font-semibold text-gray-900 text-center hover:bg-gray-100">
               Get Started
             </NuxtLink>
             <button v-else disabled class="mt-8 block w-full bg-gray-50 border border-gray-200 rounded-md py-3 text-sm font-semibold text-gray-400 text-center cursor-not-allowed">
               Current Plan
             </button>
          </div>

          <!-- Pro Tier -->
          <div class="bg-white rounded-2xl shadow-xl border-2 border-blue-600 p-8 flex flex-col relative overflow-hidden">
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
            <p class="mt-4 text-gray-500">Unlock your full potential.</p>
            <ul class="mt-6 space-y-4 flex-1">
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-900 font-medium">Everything in Free</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Premium "Modern" Themes</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Advanced Analytics</span>
              </li>
              <li class="flex items-start">
                <svg class="flex-shrink-0 h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span class="ml-3 text-gray-500">Verified Badge (Coming Soon)</span>
              </li>
            </ul>
             <NuxtLink v-if="!isLoggedIn" to="/register?plan=pro" class="mt-8 block w-full bg-blue-600 border border-transparent rounded-md py-3 text-sm font-semibold text-white text-center hover:bg-blue-700 shadow-md">
               Upgrade to Pro
             </NuxtLink>
             <NuxtLink v-else to="/cards" class="mt-8 block w-full bg-blue-600 border border-transparent rounded-md py-3 text-sm font-semibold text-white text-center hover:bg-blue-700 shadow-md">
               Upgrade Inside
             </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-16 bg-white">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-extrabold text-gray-900 text-center mb-8">Frequently Asked Questions</h2>
            <div class="space-y-6">
                <div>
                    <h3 class="text-lg font-medium text-gray-900">Is ContactShare really free?</h3>
                    <p class="mt-2 text-gray-500">Yes! The Free plan allows you to create a complete digital business card with unlimited sharing. You only pay if you want premium themes or advanced features.</p>
                </div>
                <div>
                    <h3 class="text-lg font-medium text-gray-900">How do I share my card?</h3>
                    <p class="mt-2 text-gray-500">You can share your card via a unique link (e.g., contactshare.com/c/yourname) or by letting others scan your personal QR code, available in your dashboard.</p>
                </div>
                <div>
                    <h3 class="text-lg font-medium text-gray-900">Can I cancel my Pro subscription?</h3>
                    <p class="mt-2 text-gray-500">Absolutely. You can cancel at any time from your account settings. You'll keep your Pro features until the end of the billing cycle.</p>
                </div>
                 <div>
                    <h3 class="text-lg font-medium text-gray-900">Do you offer custom domains?</h3>
                    <p class="mt-2 text-gray-500">We are working on it! Custom domains (e.g., yourname.com) will be available soon as an add-on or part of a higher tier.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Footer -->
    <section class="bg-blue-700">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          <span class="block">Ready to upgrade your networking?</span>
          <span class="block text-blue-200">Create your first card today.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <NuxtLink
              to="/register"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50"
            >
              Start for Free
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const { isLoggedIn } = useAuth()
</script>
