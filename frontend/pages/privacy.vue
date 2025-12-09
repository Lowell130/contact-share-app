<template>
  <section class="max-w-3xl mx-auto py-10 px-4">
    <h1 class="text-3xl font-bold mb-6">Privacy Policy</h1>
    <div class="prose dark:prose-invert">
      <p class="mb-4">Last updated: {{ new Date().toLocaleDateString() }}</p>

      <h2 class="text-xl font-semibold mt-6 mb-3">1. Introduction</h2>
      <p>
        Welcome to Contact Share ("we," "our," or "us"). We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you as to how we look after your personal data when you visit our website and tell you about your privacy rights and how the law protects you.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">2. Data We Collect</h2>
      <p>
        We may collect, use, store and transfer different kinds of personal data about you which we have grouped together follows:
      </p>
      <ul class="list-disc pl-5 space-y-2 mt-2">
        <li><strong>Identity Data:</strong> includes username or similar identifier, title, and avatar image.</li>
        <li><strong>Contact Data:</strong> includes email address and telephone numbers you choose to share on your cards.</li>
        <li><strong>Technical Data:</strong> includes internet protocol (IP) address, your login data, browser type and version, time zone setting and location, browser plug-in types and versions, operating system and platform, and other technology on the devices you use to access this website.</li>
      </ul>

      <h2 class="text-xl font-semibold mt-6 mb-3">3. How We Use Your Data</h2>
      <p>
        We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:
      </p>
      <ul class="list-disc pl-5 space-y-2 mt-2">
        <li>To provide the service of creating and sharing digital contact cards.</li>
        <li>To manage your account and registration.</li>
        <li>To improve our website, products/services, marketing or customer relationships.</li>
      </ul>

      <h2 class="text-xl font-semibold mt-6 mb-3">4. Data Security</h2>
      <p>
        We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">5. Your Legal Rights</h2>
      <p>
        Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to request access, correction, erasure, restriction, transfer, to object to processing, to portability of data and (where the lawful ground of processing is consent) to withdraw consent.
      </p>

      <h2 class="text-xl font-semibold mt-6 mb-3">6. Contact Us</h2>
      <p>
        If you have any questions about this privacy policy or our privacy practices, please contact us at: <a href="mailto:info@example.com" class="text-blue-600 hover:underline">info@example.com</a>.
      </p>
    </div>
  </section>
</template>

<script setup>
useHead({
  title: 'Privacy Policy - Contact Share',
  meta: [
    { name: 'description', content: 'Privacy Policy for Contact Share application.' }
  ]
})
</script>