<script lang="ts">
	import { onMount } from 'svelte';

	let role = '';

	onMount(async () => {
		const token = localStorage.getItem('access_token');
		if (!token) return window.location.href = '/auth/login';

		const res = await fetch('http://localhost:8000/api/auth/me', {
			headers: { Authorization: `Bearer ${token}` }
		});

		if (res.ok) {
			const data = await res.json();
			role = data.role;
		} else {
			localStorage.removeItem('access_token');
			window.location.href = '/auth/login';
		}
	});
</script>

<div class="flex">
	<!-- Sidebar -->
	<div class="w-64 bg-gray-800 text-white min-h-screen p-4 space-y-4">
		<h2 class="text-lg font-bold">Issue Tracker</h2>
		<a href="/dashboard" class="block hover:underline">All Issues</a>
		<a href="/dashboard/create" class="block hover:underline">Create Issue</a>
		<a href="/dashboard/analytics" class="block hover:underline">Analytics</a>

		{#if role === 'ADMIN'}
			<a href="/dashboard/admin" class="block hover:underline text-yellow-300">Admin Panel</a>
		{/if}

		<button class="mt-4 bg-red-600 px-3 py-1 rounded" on:click={() => {
			localStorage.removeItem('access_token');
			window.location.href = '/auth/login';
		}}>Logout</button>
	</div>

	<!-- Main content -->
	<div class="flex-1 p-6">
		<slot />
	</div>
</div>
