<!-- frontend/src/routes/+layout.svelte -->
<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth';
	import { websocketStore } from '$lib/stores/websocket';
	import Navigation from '$lib/stores/components/Navigation.svelte';
	import Toast from '../lib/stores/components/Toast.svelte';
	
	let mounted = false;
	
	onMount(() => {
	  mounted = true;
	  
	  // Initialize auth
	  authStore.initAuth();
	  
	  // Connect to WebSocket when authenticated
	  authStore.subscribe(({ isAuthenticated, token }) => {
		if (isAuthenticated && token) {
		  websocketStore.connect(token);
		} else {
		  websocketStore.disconnect();
		}
	  });
	});
	
	$: isAuthRoute = $page.route.id?.startsWith('/(auth)');
  </script>
  
  <svelte:head>
	<title>Issues & Insights Tracker</title>
	<meta name="description" content="Track and manage issues with real-time updates" />
  </svelte:head>
  
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
	{#if mounted}
	  {#if !isAuthRoute && $authStore.isAuthenticated}
		<Navigation />
		<main class="container mx-auto px-4 py-8">
		  <slot />
		</main>
	  {:else}
		<slot />
	  {/if}
	{:else}
	  <div class="flex items-center justify-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
	  </div>
	{/if}
	
	<Toast />
  </div>