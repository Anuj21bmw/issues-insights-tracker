<script lang="ts">
	import { onMount } from 'svelte';

	let email = '';
	let password = '';

	onMount(() => {
		const token = localStorage.getItem('access_token');
		if (token) {
			window.location.href = '/dashboard';
		}
	});

	const handleLogin = async () => {
		const formData = new URLSearchParams();
		formData.append('username', email);
		formData.append('password', password);

		const res = await fetch('http://localhost:8000/api/auth/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: formData.toString(),
		});

		const data = await res.json();
		if (res.ok) {
			localStorage.setItem('access_token', data.access_token);
			alert('Login successful!');
			window.location.href = '/dashboard';
		} else {
			alert(data.detail || 'Login failed.');
		}
	};
</script>


<h2 class="text-2xl font-bold mb-4">Login</h2>
<div class="flex flex-col gap-2 max-w-sm">
	<input class="border p-2 rounded" bind:value={email} placeholder="Email" />
	<input class="border p-2 rounded" type="password" bind:value={password} placeholder="Password" />
	<button on:click={handleLogin} class="bg-blue-600 text-white p-2 rounded">Login</button>
</div>
