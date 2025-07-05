<script lang="ts">
	import { onMount } from 'svelte'; // ✅ Required

	let user: any = null;

	onMount(async () => {
		const token = localStorage.getItem('access_token');
		if (!token) {
			alert('Not logged in!');
			window.location.href = '/auth/login';
			return;
		}

		const res = await fetch('http://localhost:8000/api/auth/me', {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		if (res.ok) {
			user = await res.json();
		} else {
			alert('Unauthorized. Please login again.');
			localStorage.removeItem('access_token');
			window.location.href = '/auth/login';
		}
	});
</script>


{#if user}
	<h1 class="text-2xl font-bold mb-4">Welcome, {user.fullName}!</h1>
	<p>Email: {user.email}</p>
	<p>Role: {user.role}</p>
{/if}
