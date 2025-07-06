<!-- src/routes/auth/register/+page.svelte -->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { toasts } from '$lib/stores/toast';
	
	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let role = 'REPORTER';
	let isLoading = false;
	let error = '';
  
	async function handleSubmit(event: Event): Promise<void> {
	  event.preventDefault();
	  
	  if (password !== confirmPassword) {
		error = 'Passwords do not match';
		toasts.error('Validation Error', error);
		return;
	  }
  
	  if (password.length < 6) {
		error = 'Password must be at least 6 characters long';
		toasts.error('Validation Error', error);
		return;
	  }
  
	  isLoading = true;
	  error = '';
  
	  try {
		const response = await fetch('http://localhost:8000/api/auth/register', {
		  method: 'POST',
		  headers: {
			'Content-Type': 'application/json'
		  },
		  body: JSON.stringify({
			name,
			email,
			password,
			role
		  })
		});
  
		if (response.ok) {
		  const data = await response.json();
		  localStorage.setItem('access_token', data.access_token);
		  toasts.success('Welcome!', 'Your account has been created successfully');
		  goto('/dashboard');
		} else {
		  const data = await response.json();
		  error = data.detail || 'Registration failed';
		  toasts.error('Registration Failed', error);
		}
	  } catch (err) {
		error = 'Network error. Please try again.';
		toasts.error('Network Error', error);
	  } finally {
		isLoading = false;
	  }
	}
  </script>
  
  <svelte:head>
	<title>Create Account - Issue Tracker</title>
  </svelte:head>
  
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
	  <div>
		<div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100">
		  <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
		  </svg>
		</div>
		<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
		  Create your account
		</h2>
		<p class="mt-2 text-center text-sm text-gray-600">
		  Or
		  <a href="/auth/login" class="font-medium text-blue-600 hover:text-blue-500">
			sign in to your existing account
		  </a>
		</p>
	  </div>
	  
	  <form class="mt-8 space-y-6" on:submit={handleSubmit}>
		<div class="space-y-4">
		  <div>
			<label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
			<input
			  id="name"
			  name="name"
			  type="text"
			  autocomplete="name"
			  required
			  bind:value={name}
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
			  placeholder="Enter your full name"
			/>
		  </div>
  
		  <div>
			<label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
			<input
			  id="email"
			  name="email"
			  type="email"
			  autocomplete="email"
			  required
			  bind:value={email}
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
			  placeholder="Enter your email address"
			/>
		  </div>
  
		  <div>
			<label for="role" class="block text-sm font-medium text-gray-700">Role</label>
			<select
			  id="role"
			  name="role"
			  bind:value={role}
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
			>
			  <option value="REPORTER">Reporter</option>
			  <option value="MAINTAINER">Maintainer</option>
			  <option value="ADMIN">Admin</option>
			</select>
			<p class="mt-1 text-xs text-gray-500">
			  Choose your role in the organization
			</p>
		  </div>
  
		  <div>
			<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
			<input
			  id="password"
			  name="password"
			  type="password"
			  autocomplete="new-password"
			  required
			  bind:value={password}
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
			  placeholder="Create a password"
			/>
			<p class="mt-1 text-xs text-gray-500">
			  Must be at least 6 characters long
			</p>
		  </div>
  
		  <div>
			<label for="confirm-password" class="block text-sm font-medium text-gray-700">Confirm Password</label>
			<input
			  id="confirm-password"
			  name="confirm-password"
			  type="password"
			  autocomplete="new-password"
			  required
			  bind:value={confirmPassword}
			  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
			  placeholder="Confirm your password"
			/>
		  </div>
		</div>
  
		{#if error}
		  <div class="rounded-md bg-red-50 p-4">
			<div class="flex">
			  <div class="flex-shrink-0">
				<svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
				  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
				</svg>
			  </div>
			  <div class="ml-3">
				<h3 class="text-sm font-medium text-red-800">
				  {error}
				</h3>
			  </div>
			</div>
		  </div>
		{/if}
  
		<div>
		  <button
			type="submit"
			disabled={isLoading}
			class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
		  >
			<span class="absolute left-0 inset-y-0 flex items-center pl-3">
			  {#if isLoading}
				<div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
			  {:else}
				<svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
				  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
				</svg>
			  {/if}
			</span>
			{isLoading ? 'Creating account...' : 'Create account'}
		  </button>
		</div>
  
		<div class="text-center">
		  <p class="text-xs text-gray-500">
			By creating an account, you agree to our
			<a href="/terms" class="text-blue-600 hover:text-blue-500">Terms of Service</a>
			and
			<a href="/privacy" class="text-blue-600 hover:text-blue-500">Privacy Policy</a>
		  </p>
		</div>
	  </form>
	</div>
  </div>