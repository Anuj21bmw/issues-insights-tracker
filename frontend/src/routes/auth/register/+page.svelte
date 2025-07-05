<script lang="ts">
	import { onMount } from 'svelte';

	let name = '';
	let email = '';
	let password = '';
	let role = 'REPORTER';

	// Redirect if already logged in
	onMount(() => {
		const token = localStorage.getItem('access_token');
		if (token) {
			window.location.href = '/dashboard';
		}
	});

	const handleRegister = async () => {
		const res = await fetch('http://localhost:8000/api/auth/register', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, email, password, role })
		});

		const data = await res.json();
		if (res.ok) {
			alert('Registration Successful!');
			window.location.href = '/auth/login';
		} else {
			alert(data.detail || 'Registration failed.');
		}
	};
</script>


<h2 class="text-2xl font-bold mb-4">Register</h2>
<div class="flex flex-col gap-2 max-w-sm">
	<input class="border p-2 rounded" bind:value={name} placeholder="Full Name" />
	<input class="border p-2 rounded" bind:value={email} placeholder="Email" />
	<input class="border p-2 rounded" type="password" bind:value={password} placeholder="Password" />
	<select bind:value={role} class="border p-2 rounded">
		<option value="ADMIN">Admin</option>
		<option value="MAINTAINER">Maintainer</option>
		<option value="REPORTER">Reporter</option>
	</select>
	<button on:click={handleRegister} class="bg-blue-600 text-white p-2 rounded">Register</button>
</div>
