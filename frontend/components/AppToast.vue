<!-- components/AppToast.vue -->
<template>
  <div
    class="fixed bottom-4 right-4 z-50 flex flex-col gap-3 pointer-events-none"
  >
    <transition-group name="toast-fade" tag="div">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="pointer-events-auto flex items-center w-full max-w-sm p-4 text-body bg-neutral-primary-soft rounded-base shadow-xs border border-default"
        role="alert"
      >
        <!-- ICONA A SINISTRA (success / danger / warning) -->
        <div
          class="inline-flex items-center justify-center shrink-0 w-7 h-7 rounded"
          :class="iconWrapperClass(t.type)"
        >
          <!-- icona success -->
          <svg
            v-if="t.type === 'success'"
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 11.917 9.724 16.5 19 7.5"
            />
          </svg>

          <!-- icona danger -->
          <svg
            v-else-if="t.type === 'danger'"
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18 17.94 6M18 18 6.06 6"
            />
          </svg>

          <!-- icona warning -->
          <svg
            v-else
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 13V8m0 8h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>

          <span class="sr-only">
            <!-- solo per accessibilità -->
            {{ srLabel(t.type) }}
          </span>
        </div>

        <!-- TESTO -->
        <div class="ms-3 text-sm font-normal">
          {{ t.message }}
        </div>

        <!-- BOTTONE CHIUDI -->
        <button
          type="button"
          class="ms-auto flex items-center justify-center text-body hover:text-heading bg-transparent box-border border border-transparent hover:bg-neutral-secondary-medium focus:ring-4 focus:ring-neutral-tertiary font-medium leading-5 rounded text-sm h-8 w-8 focus:outline-none"
          @click="remove(t.id)"
          aria-label="Close"
        >
          <span class="sr-only">Close</span>
          <svg
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18 17.94 6M18 18 6.06 6"
            />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useToast } from '~/composables/useToast'

const { toasts, remove } = useToast()

const iconWrapperClass = (type) => {
  if (type === 'success') {
    return 'text-fg-success bg-success-soft'
  }
  if (type === 'danger') {
    return 'text-fg-danger bg-danger-soft'
  }
  // default warning
  return 'text-fg-warning bg-warning-soft'
}

const srLabel = (type) => {
  if (type === 'success') return 'Success'
  if (type === 'danger') return 'Error'
  return 'Warning'
}
</script>

<style scoped>
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.2s ease-out;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
