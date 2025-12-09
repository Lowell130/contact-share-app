<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 p-4">
      <slot />
    </main>
    <AppFooter />
       <!-- Host globale dei toast -->
    <AppToast />
    <CookieBanner />
  </div>
</template>

<script setup>
import AppHeader from '~/components/AppHeader.vue'
import AppFooter from '~/components/AppFooter.vue'
import AppToast from '~/components/AppToast.vue'
import CookieBanner from '~/components/CookieBanner.vue'
</script>
