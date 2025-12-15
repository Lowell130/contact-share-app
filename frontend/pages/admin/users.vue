<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <div class="px-4 py-5 sm:px-6 flex justify-between items-center border-b border-gray-200">
       <h3 class="text-lg leading-6 font-medium text-gray-900">Registered Users</h3>
       <div class="flex gap-2">
           <input v-model="search" @keyup.enter="loadUsers" type="text" placeholder="Search..." class="border border-gray-300 rounded-md px-3 py-1 text-sm" />
           <button @click="loadUsers" class="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200 text-sm">Refresh</button>
       </div>
    </div>
    
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name/Email</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Plan</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="u in users" :key="u.id">
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900">{{ u.name || 'No Name' }}</div>
                        <div class="text-sm text-gray-500">{{ u.email }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                         <span 
                            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                            :class="{
                                'bg-green-100 text-green-800': u.plan === 'pro',
                                'bg-gray-100 text-gray-800': u.plan === 'free',
                                'bg-red-100 text-red-800': u.plan === 'admin'
                            }"
                        >
                            {{ u.plan.toUpperCase() }}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ new Date(u.created_at).toLocaleDateString() }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <select 
                            :value="u.plan" 
                            @change="changePlan(u, $event.target.value)"
                            class="text-xs border-gray-300 rounded shadow-sm focus:ring-blue-500 focus:border-blue-500 mr-2"
                        >
                            <option value="free">Free</option>
                            <option value="pro">Pro</option>
                            <option value="admin">Admin</option>
                        </select>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin', middleware: 'admin' })
const { $api } = useApi()
const toast = useToast()

const users = ref([])
const search = ref('')

async function loadUsers() {
    try {
        const q = search.value ? `?q=${encodeURIComponent(search.value)}` : ''
        users.value = await $api(`/admin/users${q}`)
    } catch(e) {
        toast.error("Failed to load users")
    }
}

async function changePlan(user, newPlan) {
    if (!confirm(`Change plan for ${user.email} to ${newPlan}?`)) return
    try {
        await $api(`/admin/users/${user.id}`, {
            method: 'PUT',
            body: { plan: newPlan }
        })
        user.plan = newPlan
        toast.success("Plan updated")
    } catch(e) {
        toast.error("Update failed")
    }
}

onMounted(loadUsers)
</script>
