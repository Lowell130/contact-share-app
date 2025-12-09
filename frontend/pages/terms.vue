<template>
  <section class="max-w-3xl mx-auto py-10 px-4">
    <h1 class="text-3xl font-bold mb-6">Terms of Service</h1>
    <div class="prose dark:prose-invert">
      <p class="mb-4">Last updated: {{ new Date().toLocaleDateString() }}</p>

      <h2 class="text-xl font-semibold mt-6 mb-3">1. Agreement to Terms</h2>
      <p>
        By accessing our website, you agree to be bound by these Terms of Service and to comply with all applicable laws and regulations. If you do not agree with these terms, you are prohibited from using or accessing this site.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">2. Use License</h2>
      <p>
        Permission is granted to temporarily download one copy of the materials (information or software) on Contact Share's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
      </p>
      <ul class="list-disc pl-5 space-y-2 mt-2">
        <li>modify or copy the materials;</li>
        <li>use the materials for any commercial purpose, or for any public display (commercial or non-commercial);</li>
        <li>attempt to decompile or reverse engineer any software contained on Contact Share's website;</li>
        <li>remove any copyright or other proprietary notations from the materials; or</li>
        <li>transfer the materials to another person or "mirror" the materials on any other server.</li>
      </ul>

      <h2 class="text-xl font-semibold mt-6 mb-3">3. User Content</h2>
      <p>
        You retain ownership of any content you submit, post, or display on or through the Service. You grant us a worldwide, non-exclusive, royalty-free license to use, copy, reproduce, process, adapt, modify, publish, transmit, display and distribute such Content in any and all media or distribution methods.
      </p>
      <p class="mt-2">
        You represent and warrant that you have all the rights, power and authority necessary to grant the rights granted herein to any Content that you submit.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">4. Disclaimer</h2>
      <p>
        The materials on Contact Share's website are provided on an 'as is' basis. Contact Share makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">5. Limitations</h2>
      <p>
        In no event shall Contact Share or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Contact Share's website, even if Contact Share or a Contact Share authorized representative has been notified orally or in writing of the possibility of such damage.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">6. Governing Law</h2>
      <p>
        These terms and conditions are governed by and construed in accordance with the laws and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
      </p>
    </div>
  </section>
</template>

<script setup>
useHead({
  title: 'Terms of Service - Contact Share',
  meta: [
    { name: 'description', content: 'Terms of Service for Contact Share application.' }
  ]
})
</script>