<!-- components/PublicCardModern.vue -->
<template>
  <section class="bg-white dark:bg-gray-900">
    <div class="flex items-center justify-center min-h-screen py-6">
      <!-- Main Card Container -->
      <div
        class="bg-white p-6 rounded-lg shadow-lg dark:bg-gray-900 border-solid border border-gray-200"
      >
        <div
          class="w-full sm:w-[550px] p-4 bg-white sm:p-6 dark:bg-gray-800 mx-auto rounded-lg"
        >
      
    <!-- HEADER / AVATAR / TITOLO + INFO -->
    <div class="pb-4 md:pb-4">
      <div class="flex flex-col md:flex-row md:items-center md:gap-6">
        <!-- Avatar -->
        <div class="flex justify-center md:justify-start">
          <div
            class="relative w-32 h-32 md:w-36 md:h-36 rounded-full overflow-hidden
                   shadow-sm bg-neutral-50
                   ring-1 ring-gray-200 
                   outline outline-[6px] outline-gray-100"
          >
            <img
              v-if="card.avatar_url"
              :src="card.avatar_url"
              :alt="card.title"
              class="absolute inset-0 w-full h-full object-cover"
            />
            <img
              v-else
              src="/assets/images/profile-picture-3.jpg"
              alt="Profile"
              class="absolute inset-0 w-full h-full object-cover"
            />
          </div>
        </div>

        <!-- Testi principali -->
        <div class="mt-4 md:mt-0 w-full text-center md:text-left space-y-3">
          <!-- Titolo -->
          <h5 class="text-2xl md:text-3xl font-bold tracking-tight text-gray-700 dark:text-white">
            {{ card.title }}
          </h5>

          <!-- Ruolo / Azienda -->
          <div
            v-if="subtitle"
            class="shadow justify-center md:justify-start rounded-full inline-flex items-center px-2 py-1 ring-1 ring-inset text-sm font-medium"
            :class="[colors.badgeBg, colors.badgeText, colors.badgeRing]"
          >
             <span>{{ subtitle }}</span>
          </div>

          <!-- INFO PRINCIPALI (email / telefono / sito) -->
          <div class="mt-2 space-y-1.5 text-sm text-gray-700 dark:text-gray-300">
            <!-- Email -->
            <div
              v-if="primary.email"
              class="flex items-center justify-center md:justify-start gap-2"
            >
              <span
                class="inline-flex items-center justify-center w-7 h-7 rounded-full"
                :class="[colors.iconBg, colors.iconText]"
                aria-hidden="true"
              >
                <!-- icona email -->
                <svg class="w-[18px] h-[18px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" stroke-linecap="round" stroke-width="1" d="m3.5 5.5 7.893 6.036a1 1 0 0 0 1.214 0L20.5 5.5M4 19h16a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1Z"/>
                </svg>
              </span>
              <a
                :href="`mailto:${primary.email}`"
                class="underline decoration-gray-300 transition-colors"
                :class="colors.linkHover"
              >
                {{ primary.email }}
              </a>
            </div>

            <!-- Telefono -->
            <div
              v-if="primary.phone"
              class="flex items-center justify-center md:justify-start gap-2"
            >
              <span
                class="inline-flex items-center justify-center w-7 h-7 rounded-full"
                :class="[colors.iconBg, colors.iconText]"
                aria-hidden="true"
              >
                <!-- icona telefono -->
                <svg class="w-[18px] h-[18px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M18.427 14.768 17.2 13.542a1.733 1.733 0 0 0-2.45 0l-.613.613a1.732 1.732 0 0 1-2.45 0l-1.838-1.84a1.735 1.735 0 0 1 0-2.452l.612-.613a1.735 1.735 0 0 0 0-2.452L9.237 5.572a1.6 1.6 0 0 0-2.45 0c-3.223 3.2-1.702 6.896 1.519 10.117 3.22 3.221 6.914 4.745 10.12 1.535a1.601 1.601 0 0 0 0-2.456Z"/>
                </svg>
              </span>
              <a
                :href="`tel:${primary.phone.replace(/\\s+/g, '')}`"
                class="underline decoration-gray-300 transition-colors"
                :class="colors.linkHover"
              >
                {{ primary.phone }}
              </a>
            </div>

            <!-- Website -->
            <div
              v-if="primary.website"
              class="flex items-center justify-center md:justify-start gap-2"
            >
              <span
                class="inline-flex items-center justify-center w-7 h-7 rounded-full"
                :class="[colors.iconBg, colors.iconText]"
                aria-hidden="true"
              >
                <!-- icona globe -->
                <svg class="w-[18px] h-[18px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" stroke-linecap="round" stroke-width="1" d="M4.37 7.657c2.063.528 2.396 2.806 3.202 3.87 1.07 1.413 2.075 1.228 3.192 2.644 1.805 2.289 1.312 5.705 1.312 6.705M20 15h-1a4 4 0 0 0-4 4v1M8.587 3.992c0 .822.112 1.886 1.515 2.58 1.402.693 2.918.351 2.918 2.334 0 .276 0 2.008 1.972 2.008 2.026.031 2.026-1.678 2.026-2.008 0-.65.527-.9 1.177-.9H20M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
                </svg>
              </span>
              <a
                :href="primary.websiteHref"
                target="_blank"
                rel="noopener"
                class="underline decoration-gray-300 transition-colors"
                :class="colors.linkHover"
              >
                {{ primary.website }}
              </a>
            </div>
          </div>
        </div>
      </div>

    <!-- separatore -->
    <div class="inline-flex items-center justify-center w-full">
        <hr class="w-64 h-1 my-8 bg-gray-200 border-0 rounded-sm dark:bg-gray-700">
        <div class="absolute px-4 -translate-x-1/2 left-1/2 bg-white dark:bg-gray-800">
            <svg class="w-6 h-6 text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11V8a1 1 0 0 0-1-1H6a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1Zm0 0v2a4 4 0 0 1-4 4H5m14-6V8a1 1 0 0 0-1-1h-3a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1Zm0 0v2a4 4 0 0 1-4 4h-1"/></svg>
        </div>
    </div>

      <!-- BIO / NOTE -->
      <p
        v-if="card.notes"
        class="mt-3 mb-4 font-light text-gray-500 dark:text-gray-400 text-sm"
      >
        {{ card.notes }}
      </p>
    </div>

          <!-- SOLO SOCIAL NELLA LISTA -->
          <PublicSocialList
            :card-title="card.title"
            :card-id="card.id"
            :fields="visibleFields"
          />
     

          <!-- BLOCCO CONDIVISIONE / QR + VCARD -->
          <div class="mt-6">
           <div
            class="relative overflow-hidden rounded-2xl border border-gray-200/80
                   px-4 py-4 sm:px-6 sm:py-5 shadow-sm"
            :class="colors.gradientBox"
          >
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

              <!-- QR + testo esplicativo -->
              <div class="flex items-center gap-4 md:gap-5">
                <!-- QR incorniciato -->
                <div class="relative shrink-0">
                  <div
                    class="rounded-2xl bg-white/90 border border-white shadow-md
                           p-2"
                  >
                    <img
                      :src="qrUrl"
                      :alt="`QR code dei contatti di ${card.title}`"
                      class="w-25 h-25 sm:w-32 sm:h-32 rounded-md"
                    />
                  </div>
                </div>

                <!-- Testo -->
                <div class="text-sm text-gray-700">
                  <p class="text-[11px] font-semibold uppercase tracking-[0.18em] mb-1" :class="colors.accentText">
                    Condividi il profilo
                  </p>
                  <p class="text-sm font-medium">
                    Inquadra il QR per aprire questo biglietto digitale.
                  </p>
                  <p class="mt-1 text-xs text-gray-500">
                    Ideale per badge, firma email, slide o social.
                  </p>
                </div>
              </div>

              <!-- Azione vCard -->
              <div
             class="flex flex-col md:flex-col justify-center items-center md:items-end gap-2 mt-1 md:mt-0"
              >
                <a
                  v-if="showVcard"
                  :href="vcardUrl"
                  class="inline-flex items-center justify-center
                         text-xs font-medium leading-5
                         bg-white
                         box-border border border-gray-200
                         shadow-xs rounded-full px-4 py-2
                         focus:outline-none transition-colors"
                  :class="[colors.btnHoverText, colors.btnHoverBg, colors.btnRing]"
                >
                  <!-- piccola icona rubrica -->
                  Scarica vCard
                </a>

                <p
                  v-if="showVcard"
                  class="text-[11px] text-gray-500 md:text-right"
                >
                  Aggiungi subito <span class="font-medium">{{ card.title }}</span>
                  alla tua rubrica.
                </p>
              </div>
            </div>
          </div>
        </div>

        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import PublicSocialList from "~/components/PublicSocialList.vue";

const props = defineProps({
  card: { type: Object, required: true },
  vcardUrl: { type: String, required: true },
  qrUrl: { type: String, required: true },
  visibleFields: { type: Array, required: true },
  // e.g. "modern_emerald", "modern_blue", "modern_indigo", ...
  themeName: { type: String, default: "modern_emerald" }, 
});

/* --------------------------------
 *  COLOR THEMES CONFIG
 * -------------------------------- */
const THEMES = {
  emerald: {
    badgeBg: "bg-emerald-50",
    badgeText: "text-emerald-700",
    badgeRing: "ring-emerald-600/20",
    iconBg: "bg-emerald-50",
    iconText: "text-emerald-600",
    linkHover: "hover:decoration-emerald-400 hover:text-emerald-600",
    accentText: "text-emerald-600",
    gradientBox: "bg-gradient-to-br from-slate-50 via-white to-emerald-50",
    btnHoverText: "text-gray-700 hover:text-emerald-700",
    btnHoverBg: "hover:bg-emerald-50",
    btnRing: "focus:ring-2 focus:ring-emerald-500/20"
  },
  blue: {
    badgeBg: "bg-blue-50",
    badgeText: "text-blue-700",
    badgeRing: "ring-blue-600/20",
    iconBg: "bg-blue-50",
    iconText: "text-blue-600",
    linkHover: "hover:decoration-blue-400 hover:text-blue-600",
    accentText: "text-blue-600",
    gradientBox: "bg-gradient-to-br from-slate-50 via-white to-blue-50",
    btnHoverText: "text-gray-700 hover:text-blue-700",
    btnHoverBg: "hover:bg-blue-50",
    btnRing: "focus:ring-2 focus:ring-blue-500/20"
  },
  indigo: {
    badgeBg: "bg-indigo-50",
    badgeText: "text-indigo-700",
    badgeRing: "ring-indigo-600/20",
    iconBg: "bg-indigo-50",
    iconText: "text-indigo-600",
    linkHover: "hover:decoration-indigo-400 hover:text-indigo-600",
    accentText: "text-indigo-600",
    gradientBox: "bg-gradient-to-br from-slate-50 via-white to-indigo-50",
    btnHoverText: "text-gray-700 hover:text-indigo-700",
    btnHoverBg: "hover:bg-indigo-50",
    btnRing: "focus:ring-2 focus:ring-indigo-500/20"
  },
  rose: {
    badgeBg: "bg-rose-50",
    badgeText: "text-rose-700",
    badgeRing: "ring-rose-600/20",
    iconBg: "bg-rose-50",
    iconText: "text-rose-600",
    linkHover: "hover:decoration-rose-400 hover:text-rose-600",
    accentText: "text-rose-600",
    gradientBox: "bg-gradient-to-br from-slate-50 via-white to-rose-50",
    btnHoverText: "text-gray-700 hover:text-rose-700",
    btnHoverBg: "hover:bg-rose-50",
    btnRing: "focus:ring-2 focus:ring-rose-500/20"
  },
  orange: {
    badgeBg: "bg-orange-50",
    badgeText: "text-orange-700",
    badgeRing: "ring-orange-600/20",
    iconBg: "bg-orange-50",
    iconText: "text-orange-600",
    linkHover: "hover:decoration-orange-400 hover:text-orange-600",
    accentText: "text-orange-600",
    gradientBox: "bg-gradient-to-br from-slate-50 via-white to-orange-50",
    btnHoverText: "text-gray-700 hover:text-orange-700",
    btnHoverBg: "hover:bg-orange-50",
    btnRing: "focus:ring-2 focus:ring-orange-500/20"
  }
};

const colors = computed(() => {
  // Estrae "emerald" da "modern_emerald"
  const suffix = (props.themeName || "").split("_")[1] || "emerald"; // default fallback
  return THEMES[suffix] || THEMES.emerald;
});

/* --------------------------------
 *  UTILITY BASE
 * -------------------------------- */
const showVcard = computed(
  () => !!(props.card && props.card.allow_vcard === true)
);

function firstField(fields, types) {
  const t = (types || []).map((s) => String(s).toLowerCase());
  return (fields || []).find(
    (x) => t.includes(String(x.type || "").toLowerCase()) && x.value
  );
}

function firstValue(fields, types) {
  const f = firstField(fields, types);
  return f ? String(f.value || "") : "";
}

function normalizeUrl(v) {
  const s = String(v || "").trim();
  if (!s) return "";
  return /^https?:\/\//i.test(s) ? s : `https://${s}`;
}

/* --------------------------------
 *  SOTTOTITOLO E INFO PRINCIPALI
 * -------------------------------- */
const subtitle = computed(() => {
  const role = firstValue(props.visibleFields, ["role", "title", "job"]);
  const company = firstValue(props.visibleFields, [
    "company",
    "org",
    "organization",
  ]);
  if (role && company) return `${role} – ${company}`;
  return role || company || "";
});

const primary = computed(() => {
  const email = firstValue(props.visibleFields, ["email"]);
  const phone = firstValue(props.visibleFields, ["mobile", "phone", "tel"]);
  const websiteField = firstField(props.visibleFields, [
    "url",
    "website",
    "site",
    "link",
  ]);
  const website = websiteField ? String(websiteField.value || "") : "";
  return {
    email,
    phone,
    website,
    websiteHref: website ? normalizeUrl(website) : "",
  };
});
</script>
