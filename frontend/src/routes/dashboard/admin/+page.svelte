<script lang="ts">
	import { onMount } from 'svelte';

	let role = '';

	onMount(() => {
		const token = localStorage.getItem('access_token');
		if (!token) return window.location.href = '/auth/login';

		fetch('http://localhost:8000/api/auth/me', {
			headers: { Authorization: `Bearer ${token}` }
		})
			.then(res => res.json())
			.then(data => {
				if (data.role !== 'ADMIN') {
					alert('Access denied');
					window.location.href = '/dashboard';
				} else {
					role = 'ADMIN';
				}
			});
	});
</script>

<h2 class="text-2xl font-bold mb-4">Admin Panel</h2>
<p class="text-gray-600">Only visible to admins.</p>
