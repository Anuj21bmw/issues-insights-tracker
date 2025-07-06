<!-- src/routes/+layout.svelte -->
<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth';
	import { toastStore } from '$lib/stores/toast';
	import { apiClient } from '$lib/api/client';
	import ToastContainer from '$lib/stores/components/ToastContainer.svelte';
	import Navigation from '$lib/stores/components/Navigation.svelte';
	
	let mounted = false;
	
	onMount(async () => {
	  // Initialize auth from localStorage
	  authStore.init();
	  
	  // Try to fetch current user if we have a token
	  const currentAuth = authStore;
	  authStore.subscribe(async (auth) => {
		if (auth.token && auth.isAuthenticated && !auth.user && !auth.loading) {
		  authStore.setLoading(true);
		  try {
			const response = await apiClient.getCurrentUser();
			if (response.data) {
			  authStore.updateUser(response.data);
			} else {
			  // Token is invalid
			  authStore.logout();
			}
		  } catch (error) {
			console.error('Failed to fetch current user:', error);
			authStore.logout();
		  } finally {
			authStore.setLoading(false);
		  }
		}
	  });
	  
	  mounted = true;
	});
  </script>
  
  {#if mounted}
	<div class="min-h-screen bg-gray-50">
	  <Navigation />
	  
	  <main>
		<slot />
	  </main>
	  
	  <ToastContainer />
	</div>
  {:else}
	<!-- Loading screen -->
	<div class="flex min-h-screen items-center justify-center bg-gray-50">
	  <div class="text-center">
		<div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
		<p class="mt-4 text-gray-600">Loading...</p>
	  </div>
	</div>
  {/if}