<!-- src/routes/auth/login/+page.svelte -->
<script lang="ts">
	import { authStore } from '$lib/stores/auth';
	import { toastStore } from '$lib/stores/toast';
	import { apiClient } from '$lib/api/client';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	
	let email = '';
	let password = '';
	let loading = false;
	let showPassword = false;
	
	$: isAuthenticated = $authStore.isAuthenticated;
	$: canSubmit = email.trim().length > 0 && password.length > 0 && !loading;
	
	onMount(() => {
	  if (isAuthenticated) {
		goto('/issues');
	  }
	});
	
	async function handleSubmit() {
  if (!canSubmit) return;

  try {
    loading = true;

    // 🔐 Login and receive token
    const response = await apiClient.login({ email: email.trim(), password });

    if (response.data) {
      const token = response.data.access_token;

      // ⚙️ Set token early to authStore (so headers include it before fetching user)
      authStore.login(token, null); // temp set

      // 👤 Fetch current user with token now in authStore
      const userResponse = await apiClient.getCurrentUser();

      if (userResponse.data) {
        // ✅ Finalize user info in authStore
        authStore.updateUser(userResponse.data);

        toastStore.success('Welcome back!');
        goto('/issues');
      } else {
        toastStore.error('Failed to fetch user info');
        authStore.clear(); // fallback if user fetch fails
      }
    } else {
      toastStore.error(response.error || 'Login failed');
    }
  } catch (error) {
    console.error('Login error:', error);
    toastStore.error('Network error. Please try again.');
  } finally {
    loading = false;
  }
}

	
	function togglePasswordVisibility() {
	  showPassword = !showPassword;
	}
  </script>
  
  <svelte:head>
	<title>Sign In - Issue Tracker</title>
  </svelte:head>
  
  <div class="flex min-h-screen items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
	<div class="w-full max-w-md space-y-8">
	  <!-- Header -->
	  <div>
		<div class="mx-auto h-12 w-12 flex items-center justify-center rounded-lg bg-blue-600">
		  <span class="text-white text-xl font-bold">🐛</span>
		</div>
		<h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
		  Sign in to your account
		</h2>
		<p class="mt-2 text-center text-sm text-gray-600">
		  Or
		  <a href="/auth/register" class="font-medium text-blue-600 hover:text-blue-500">
			create a new account
		  </a>
		</p>
	  </div>
  
	  <!-- Form -->
	  <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
		<div class="space-y-4 rounded-md shadow-sm">
		  <!-- Email -->
		  <div>
			<label for="email" class="block text-sm font-medium text-gray-700 mb-1">
			  Email address
			</label>
			<input
			  id="email"
			  name="email"
			  type="email"
			  autocomplete="email"
			  required
			  bind:value={email}
			  disabled={loading}
			  placeholder="Enter your email"
			  class="relative block w-full rounded-lg border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
			/>
		  </div>
  
		  <!-- Password -->
		  <div>
			<label for="password" class="block text-sm font-medium text-gray-700 mb-1">
			  Password
			</label>
			<div class="relative">
			  <input
				id="password"
				name="password"
				type={showPassword ? 'text' : 'password'}
				autocomplete="current-password"
				required
				bind:value={password}
				disabled={loading}
				placeholder="Enter your password"
				class="relative block w-full rounded-lg border-gray-300 px-3 py-2 pr-10 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
			  />
			  <button
				type="button"
				class="absolute inset-y-0 right-0 flex items-center pr-3"
				on:click={togglePasswordVisibility}
				disabled={loading}
			  >
				{#if showPassword}
				  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
				  </svg>
				{:else}
				  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
				  </svg>
				{/if}
			  </button>
			</div>
		  </div>
		</div>
  
		<!-- Options -->
		<div class="flex items-center justify-between">
		  <div class="flex items-center">
			<input
			  id="remember-me"
			  name="remember-me"
			  type="checkbox"
			  class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
			/>
			<label for="remember-me" class="ml-2 block text-sm text-gray-900">
			  Remember me
			</label>
		  </div>
  
		  <div class="text-sm">
			<a href="/auth/forgot-password" class="font-medium text-blue-600 hover:text-blue-500">
			  Forgot your password?
			</a>
		  </div>
		</div>
  
		<!-- Submit Button -->
		<div>
		  <button
			type="submit"
			disabled={!canSubmit}
			class="group relative flex w-full justify-center rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
		  >
			{#if loading}
			  <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			  </svg>
			  Signing in...
			{:else}
			  Sign in
			{/if}
		  </button>
		</div>
	  </form>
  
	  <!-- Demo credentials -->
	  <div class="mt-6 rounded-lg bg-yellow-50 border border-yellow-200 p-4">
		<div class="flex">
		  <div class="flex-shrink-0">
			<svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
			  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
			</svg>
		  </div>
		  <div class="ml-3">
			<h3 class="text-sm font-medium text-yellow-800">Demo Account</h3>
			<div class="mt-2 text-sm text-yellow-700">
			  <p>Email: <code class="bg-yellow-100 px-1 rounded">demo@example.com</code></p>
			  <p>Password: <code class="bg-yellow-100 px-1 rounded">demo123</code></p>
			</div>
		  </div>
		</div>
	  </div>
	</div>
  </div>