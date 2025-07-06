<!-- src/routes/+page.svelte -->
<script>
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let isLoggedIn = false;

	onMount(async () => {
		if (browser) {
			const token = localStorage.getItem('access_token');
			if (token) {
				// Verify token is still valid
				try {
					const response = await fetch('http://localhost:8000/api/auth/me', {
						headers: {
							'Authorization': `Bearer ${token}`
						}
					});
					if (response.ok) {
						isLoggedIn = true;
					} else {
						localStorage.removeItem('access_token');
					}
				} catch (error) {
					localStorage.removeItem('access_token');
				}
			}
		}
	});

	function handleGetStarted() {
		if (isLoggedIn) {
			goto('/dashboard');
		} else {
			goto('/login');
		}
	}
</script>

<svelte:head>
	<title>Issue Tracker - Manage Issues Efficiently</title>
	<meta name="description" content="A powerful issue tracking system to help teams manage bugs, features, and tasks efficiently." />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
	<!-- Navigation -->
	<nav class="relative max-w-7xl mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8 py-6">
		<div class="flex items-center">
			<div class="flex items-center space-x-2">
				<div class="h-10 w-10 bg-blue-600 rounded-lg flex items-center justify-center">
					<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<span class="text-xl font-bold text-gray-900">Issue Tracker</span>
			</div>
		</div>
		
		<div class="flex items-center space-x-4">
			{#if isLoggedIn}
				<a href="/dashboard" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">
					Dashboard
				</a>
				<a href="/issues" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">
					Issues
				</a>
			{:else}
				<a href="/login" class="text-gray-600 hover:text-gray-900 font-medium transition-colors">
					Sign In
				</a>
				<a href="/register" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors">
					Get Started
				</a>
			{/if}
		</div>
	</nav>

	<!-- Hero Section -->
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
		<div class="text-center">
			<h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
				Streamline Your
				<span class="text-blue-600">Issue Tracking</span>
			</h1>
			<p class="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
				Efficiently manage bugs, feature requests, and tasks with our powerful issue tracking system. 
				Keep your team organized and your projects on track.
			</p>
			<div class="mt-10 flex justify-center space-x-4">
				<button
					on:click={handleGetStarted}
					class="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
				>
					{isLoggedIn ? 'Go to Dashboard' : 'Get Started Free'}
				</button>
				{#if !isLoggedIn}
					<a href="/login" class="border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-lg text-lg font-semibold hover:border-gray-400 hover:bg-gray-50 transition-colors">
						Sign In
					</a>
				{/if}
			</div>
		</div>

		<!-- Features Preview -->
		<div class="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
			<div class="text-center">
				<div class="mx-auto h-16 w-16 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
					<svg class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold text-gray-900 mb-3">Easy Issue Creation</h3>
				<p class="text-gray-600">
					Quickly create and organize issues with our intuitive interface. Add descriptions, set priorities, and track progress.
				</p>
			</div>

			<div class="text-center">
				<div class="mx-auto h-16 w-16 bg-green-100 rounded-xl flex items-center justify-center mb-6">
					<svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold text-gray-900 mb-3">Real-time Analytics</h3>
				<p class="text-gray-600">
					Get insights into your team's performance with comprehensive dashboards and visual analytics.
				</p>
			</div>

			<div class="text-center">
				<div class="mx-auto h-16 w-16 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
					<svg class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold text-gray-900 mb-3">Team Collaboration</h3>
				<p class="text-gray-600">
					Enable seamless collaboration with role-based access control and real-time updates.
				</p>
			</div>
		</div>
	</div>

	<!-- Stats Section -->
	<div class="bg-white py-16">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="text-center mb-12">
				<h2 class="text-3xl font-bold text-gray-900">Trusted by Development Teams</h2>
				<p class="mt-4 text-lg text-gray-600">Join thousands of teams who trust our platform</p>
			</div>
			
			<div class="grid grid-cols-2 md:grid-cols-4 gap-8">
				<div class="text-center">
					<div class="text-3xl font-bold text-blue-600">10K+</div>
					<div class="text-gray-600 font-medium">Issues Tracked</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-green-600">500+</div>
					<div class="text-gray-600 font-medium">Teams</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-purple-600">99.9%</div>
					<div class="text-gray-600 font-medium">Uptime</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-orange-600">24/7</div>
					<div class="text-gray-600 font-medium">Support</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Features Section -->
	<div class="py-16 bg-gray-50">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="text-center mb-16">
				<h2 class="text-3xl font-bold text-gray-900">Everything You Need</h2>
				<p class="mt-4 text-lg text-gray-600">Powerful features to keep your projects on track</p>
			</div>

			<div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
				<div>
					<h3 class="text-2xl font-bold text-gray-900 mb-6">Comprehensive Issue Management</h3>
					<div class="space-y-4">
						<div class="flex items-start space-x-3">
							<div class="flex-shrink-0 h-6 w-6 bg-blue-600 rounded-full flex items-center justify-center mt-0.5">
								<svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
									<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
								</svg>
							</div>
							<div>
								<h4 class="font-semibold text-gray-900">Status Tracking</h4>
								<p class="text-gray-600">Monitor issue progress from open to resolution</p>
							</div>
						</div>
						<div class="flex items-start space-x-3">
							<div class="flex-shrink-0 h-6 w-6 bg-blue-600 rounded-full flex items-center justify-center mt-0.5">
								<svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
									<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
								</svg>
							</div>
							<div>
								<h4 class="font-semibold text-gray-900">Advanced Filtering</h4>
								<p class="text-gray-600">Find issues quickly with powerful search and filters</p>
							</div>
						</div>
						<div class="flex items-start space-x-3">
							<div class="flex-shrink-0 h-6 w-6 bg-blue-600 rounded-full flex items-center justify-center mt-0.5">
								<svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
									<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
								</svg>
							</div>
							<div>
								<h4 class="font-semibold text-gray-900">Role-based Access</h4>
								<p class="text-gray-600">Control who can view and modify issues</p>
							</div>
						</div>
					</div>
				</div>
				
				<div class="bg-white rounded-2xl shadow-xl p-8">
					<div class="space-y-4">
						<div class="flex items-center justify-between p-4 bg-red-50 border border-red-200 rounded-lg">
							<div class="flex items-center space-x-3">
								<div class="h-3 w-3 bg-red-500 rounded-full"></div>
								<span class="font-medium text-gray-900">Critical Bug</span>
							</div>
							<span class="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">Open</span>
						</div>
						<div class="flex items-center justify-between p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
							<div class="flex items-center space-x-3">
								<div class="h-3 w-3 bg-yellow-500 rounded-full"></div>
								<span class="font-medium text-gray-900">Feature Request</span>
							</div>
							<span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">In Progress</span>
						</div>
						<div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
							<div class="flex items-center space-x-3">
								<div class="h-3 w-3 bg-green-500 rounded-full"></div>
								<span class="font-medium text-gray-900">Enhancement</span>
							</div>
							<span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Resolved</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- CTA Section -->
	<div class="bg-blue-600 py-16">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
			<h2 class="text-3xl font-bold text-white mb-4">
				Ready to Get Started?
			</h2>
			<p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
				Join thousands of teams who are already using our platform to streamline their issue tracking.
			</p>
			<button
				on:click={handleGetStarted}
				class="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-50 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
			>
				{isLoggedIn ? 'Go to Dashboard' : 'Start Free Trial'}
			</button>
		</div>
	</div>

	<!-- Footer -->
	<footer class="bg-gray-900 py-12">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-2">
					<div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
						<svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<span class="text-white font-semibold">Issue Tracker</span>
				</div>
				<p class="text-gray-400 text-sm">
					© 2024 Issue Tracker. Built with SvelteKit and FastAPI.
				</p>
			</div>
		</div>
	</footer>
</div>