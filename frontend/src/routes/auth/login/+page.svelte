<!-- frontend/src/routes/auth/login/+page.svelte -->
<script lang="ts">
	import { authStore } from '$lib/stores/auth';
	import { toastStore } from '$lib/stores/toast';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	
	let email = '';
	let password = '';
	let loading = false;
	
	$: isAuthenticated = $authStore.isAuthenticated;
	
	// Redirect if already authenticated
	onMount(() => {
	  if (isAuthenticated) {
		goto('/dashboard');
	  }
	});
	
	$: if (isAuthenticated) {
	  goto('/dashboard');
	}
	
	async function handleLogin() {
	  if (!email || !password) {
		toastStore.error('Please fill in all fields');
		return;
	  }
	  
	  loading = true;
	  
	  try {
		const result = await authStore.login(email, password);
		
		if (result.success) {
		  toastStore.success('Login successful!');
		} else {
		  toastStore.error(result.error || 'Login failed');
		}
	  } catch (error) {
		toastStore.error('An unexpected error occurred');
	  } finally {
		loading = false;
	  }
	}
	
	function handleKeyPress(event: KeyboardEvent) {
	  if (event.key === 'Enter') {
		handleLogin();
	  }
	}
  </script>
  
  <svelte:head>
	<title>Login - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
	  <!-- Header -->
	  <div class="text-center">
		<div class="flex justify-center">
		  <span class="text-6xl">🔍</span>
		</div>
		<h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
		  Issues & Insights Tracker
		</h2>
		<p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
		  Sign in to your account
		</p>
	  </div>
	  
	  <!-- Login Form -->
	  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-8">
		<form on:submit|preventDefault={handleLogin} class="space-y-6">
		  <!-- Email Field -->
		  <div>
			<label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
			  Email address
			</label>
			<input
			  id="email"
			  type="email"
			  bind:value={email}
			  on:keypress={handleKeyPress}
			  required
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 
					 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500
					 bg-white dark:bg-gray-700 text-gray-900 dark:text-white
					 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
			  placeholder="Enter your email"
			  disabled={loading}
			/>
		  </div>
		  
		  <!-- Password Field -->
		  <div>
			<label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
			  Password
			</label>
			<input
			  id="password"
			  type="password"
			  bind:value={password}
			  on:keypress={handleKeyPress}
			  required
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 
					 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500
					 bg-white dark:bg-gray-700 text-gray-900 dark:text-white
					 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
			  placeholder="Enter your password"
			  disabled={loading}
			/>
		  </div>
		  
		  <!-- Submit Button -->
		  <button
			type="submit"
			disabled={loading || !email || !password}
			class="w-full flex justify-center items-center py-2 px-4 border border-transparent 
				   rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 
				   hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 
				   focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed
				   transition-colors duration-200"
		  >
			{#if loading}
			  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			  </svg>
			  Signing in...
			{:else}
			  Sign in
			{/if}
		  </button>
		</form>
		
		<!-- Register Link -->
		<div class="mt-6 text-center">
		  <p class="text-sm text-gray-600 dark:text-gray-400">
			Don't have an account?
			<a
			  href="/auth/register"
			  class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 
					 dark:hover:text-blue-300 transition-colors duration-200"
			>
			  Sign up here
			</a>
		  </p>
		</div>
	  </div>
	  
	  <!-- Demo Credentials -->
	  <div class="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 text-sm">
		<h3 class="font-medium text-blue-900 dark:text-blue-100 mb-2">Demo Credentials:</h3>
		<div class="space-y-1 text-blue-800 dark:text-blue-200">
		  <p><strong>Admin:</strong> admin@example.com / admin123</p>
		  <p><strong>Maintainer:</strong> maintainer@example.com / maintainer123</p>
		  <p><strong>Reporter:</strong> reporter@example.com / reporter123</p>
		</div>
	  </div>
	</div>
  </div>