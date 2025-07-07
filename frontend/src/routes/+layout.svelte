<!-- src/routes/+layout.svelte -->
<script lang="ts">
	import '../app.css';
import { page } from '$app/stores';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import ToastContainer from '$lib/stores/components/ToastContainer.svelte';
import { toasts } from '$lib/stores/toast';
import { theme } from '$lib/stores/theme';
  
let user: any = null;
let showMobileMenu = false;
let currentTheme = 'light';
theme.subscribe((value) => currentTheme = value);
  
	onMount(() => {
	  checkAuth();
	});
  
	function checkAuth() {
	  const token = localStorage.getItem('access_token');
	  if (token) {
		// You could validate the token here
		user = { name: 'User' }; // Placeholder
	  }
	}
  
function logout() {
  localStorage.removeItem('access_token');
  user = null;
  toasts.success('Logged Out', 'You have been logged out successfully');
  goto('/auth/login');
}

function toggleTheme() {
  theme.toggle();
}
  
	function isActivePath(path: string): boolean {
	  return $page.url.pathname === path || $page.url.pathname.startsWith(path + '/');
	}
  
	$: isAuthPage = $page.url.pathname.startsWith('/auth/');
  </script>
  
  {#if !isAuthPage}
	<!-- Navigation -->
	<nav class="bg-white shadow-sm border-b border-gray-200">
	  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
		  <div class="flex">
			<!-- Logo -->
			<div class="flex-shrink-0 flex items-center">
			  <a href="/" class="text-xl font-bold text-gray-900">
				Issue Tracker
			  </a>
			</div>
  
			<!-- Desktop Navigation -->
			<div class="hidden sm:ml-6 sm:flex sm:space-x-8">
			  <a
				href="/dashboard"
				class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors {isActivePath('/dashboard') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
			  >
				Dashboard
			  </a>
			  <a
				href="/issues"
				class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors {isActivePath('/issues') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
			  >
				Issues
			  </a>
			</div>
		  </div>
  
		  <!-- Right side -->
		  <div class="hidden sm:ml-6 sm:flex sm:items-center space-x-4">
			<!-- Create Issue Button -->
                        <a
                          href="/issues/new"
                          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                        >
                          <svg class="-ml-1 mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                          </svg>
                          New Issue
                        </a>

                        <button
                          type="button"
                          class="rounded-full p-2 text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                          aria-label="Toggle dark mode"
                          on:click={toggleTheme}
                        >
                          {#if currentTheme === 'dark'}
                            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M10 2a1 1 0 01.832.445A5.978 5.978 0 005 8c0 3.314 2.686 6 6 6 1.657 0 3.157-.67 4.24-1.76A1 1 0 1116.73 14.45 8 8 0 1110 2z" />
                            </svg>
                          {:else}
                            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M10 5.5a4.5 4.5 0 110 9 4.5 4.5 0 010-9zM10 2a.75.75 0 01.75.75v1.13a.75.75 0 01-1.5 0V2.75A.75.75 0 0110 2zm0 12.37a.75.75 0 011.5 0v1.13a.75.75 0 01-1.5 0v-1.13zM15.45 7.88a.75.75 0 011.06-1.06l.8.8a.75.75 0 11-1.06 1.06l-.8-.8zM4.49 17.76a.75.75 0 01-1.06-1.06l.8-.8a.75.75 0 011.06 1.06l-.8.8zm10.96 2.65a.75.75 0 011.06 0 .75.75 0 010 1.06l-.8.8a.75.75 0 11-1.06-1.06l.8-.8zM3.64 7.88a.75.75 0 111.06-1.06l.8.8a.75.75 0 11-1.06 1.06l-.8-.8z" clip-rule="evenodd" />
                            </svg>
                          {/if}
                        </button>
  
			<!-- User Menu -->
			{#if user}
			  <div class="relative">
				<button
				  type="button"
				  class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
				  on:click={() => showMobileMenu = !showMobileMenu}
				>
				  <span class="sr-only">Open user menu</span>
				  <div class="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center">
					<svg class="h-5 w-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
					  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
					</svg>
				  </div>
				</button>
  
				{#if showMobileMenu}
				  <div class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
					<a href="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
					  Your Profile
					</a>
					<a href="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
					  Settings
					</a>
					<button
					  on:click={logout}
					  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
					>
					  Sign out
					</button>
				  </div>
				{/if}
			  </div>
			{:else}
			  <a
				href="/auth/login"
				class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
			  >
				Sign in
			  </a>
			{/if}
		  </div>
  
		  <!-- Mobile menu button -->
		  <div class="sm:hidden flex items-center">
			<button
			  type="button"
			  class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
			  on:click={() => showMobileMenu = !showMobileMenu}
			>
			  <span class="sr-only">Open main menu</span>
			  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
			  </svg>
			</button>
		  </div>
		</div>
	  </div>
  
	  <!-- Mobile menu -->
	  {#if showMobileMenu}
		<div class="sm:hidden">
		  <div class="pt-2 pb-3 space-y-1">
			<a
			  href="/dashboard"
			  class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium {isActivePath('/dashboard') ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50 hover:border-gray-300'}"
			>
			  Dashboard
			</a>
			<a
			  href="/issues"
			  class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium {isActivePath('/issues') ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50 hover:border-gray-300'}"
			>
			  Issues
			</a>
		  </div>
		  <div class="pt-4 pb-3 border-t border-gray-200">
			{#if user}
			  <div class="flex items-center px-4">
				<div class="flex-shrink-0">
				  <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
					<svg class="h-6 w-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
					  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
					</svg>
				  </div>
				</div>
				<div class="ml-3">
				  <div class="text-base font-medium text-gray-800">{user.name}</div>
				</div>
			  </div>
			  <div class="mt-3 space-y-1">
				<a href="/profile" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
				  Your Profile
				</a>
				<a href="/settings" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
				  Settings
				</a>
				<button
				  on:click={logout}
				  class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
				>
				  Sign out
				</button>
			  </div>
			{:else}
			  <div class="px-4">
				<a
				  href="/auth/login"
				  class="block text-base font-medium text-gray-500 hover:text-gray-800"
				>
				  Sign in
				</a>
			  </div>
			{/if}
		  </div>
		</div>
	  {/if}
	</nav>
  
	<!-- Main Content -->
	<main class="flex-1">
	  <div class="py-6">
		<slot />
	  </div>
	</main>
  {:else}
	<!-- Auth pages without navigation -->
	<slot />
  {/if}
  
  <!-- Toast Container -->
  <ToastContainer />
  
  <!-- Click outside handler for mobile menu -->
  {#if showMobileMenu}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div 
	  class="fixed inset-0 z-40" 
	  on:click={() => showMobileMenu = false}
	></div>
  {/if}