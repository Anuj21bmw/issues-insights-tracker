<!-- src/routes/dashboard/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import type { DashboardStats } from '$lib/types';
	import { authStore } from '$lib/stores/auth';
	import { toastStore } from '$lib/stores/toast';
	import RecentIssues from '$lib/stores/components/RecentIssues.svelte';
  
	Chart.register(...registerables);
  
	let stats: DashboardStats | null = null;
	let loading = true;
	let error = '';
	let chartCanvas: HTMLCanvasElement;
	let chart: Chart | null = null;
  
	$: isAuthenticated = $authStore.isAuthenticated;
	$: user = $authStore.user;
  
	onMount(async () => {
	  if (!isAuthenticated) {
		window.location.href = '/auth/login';
		return;
	  }
	  await loadDashboardStats();
	});
  
	async function loadDashboardStats(): Promise<void> {
	  try {
		loading = true;
		const token = localStorage.getItem('access_token');
		const response = await fetch('http://localhost:8000/api/dashboard/stats', {
		  headers: {
			'Authorization': `Bearer ${token}`
		  }
		});
  
		if (response.ok) {
		  stats = await response.json();
		  setTimeout(() => createChart(), 100); // Small delay to ensure canvas is rendered
		} else {
		  error = 'Failed to load dashboard data';
		  toastStore.error('Load Failed', 'Failed to load dashboard data');
		}
	  } catch (err) {
		error = 'Network error';
		toastStore.error('Network Error', 'Failed to connect to server');
	  } finally {
		loading = false;
	  }
	}
  
	function createChart(): void {
	  if (!stats || !chartCanvas) return;
  
	  // Destroy existing chart
	  if (chart) {
		chart.destroy();
	  }
  
	  const ctx = chartCanvas.getContext('2d');
	  if (!ctx) return;
  
	  const chartData = [
		stats.open_issues,
		stats.in_progress_issues,
		stats.resolved_issues,
		stats.closed_issues
	  ];
  
	  chart = new Chart(ctx, {
		type: 'doughnut',
		data: {
		  labels: ['Open', 'In Progress', 'Resolved', 'Closed'],
		  datasets: [{
			data: chartData,
			backgroundColor: [
			  'rgba(239, 68, 68, 0.8)',   // Red for Open
			  'rgba(245, 158, 11, 0.8)',  // Amber for In Progress
			  'rgba(34, 197, 94, 0.8)',   // Green for Resolved
			  'rgba(107, 114, 128, 0.8)'  // Gray for Closed
			],
			borderColor: [
			  'rgb(239, 68, 68)',   // Red
			  'rgb(245, 158, 11)',  // Amber
			  'rgb(34, 197, 94)',   // Green
			  'rgb(107, 114, 128)'  // Gray
			],
			borderWidth: 2,
			hoverBackgroundColor: [
			  'rgba(239, 68, 68, 0.9)',
			  'rgba(245, 158, 11, 0.9)',
			  'rgba(34, 197, 94, 0.9)',
			  'rgba(107, 114, 128, 0.9)'
			]
		  }]
		},
		options: {
		  responsive: true,
		  maintainAspectRatio: false,
		  plugins: {
			legend: {
			  position: 'bottom',
			  labels: {
				padding: 20,
				usePointStyle: true,
				font: {
				  size: 12,
				  family: 'Inter, system-ui, sans-serif'
				}
			  }
			},
			tooltip: {
			  callbacks: {
				label: function(context) {
				  const label = context.label || '';
				  const value = context.parsed;
				  const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
				  const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0';
				  return `${label}: ${value} (${percentage}%)`;
				}
			  },
			  backgroundColor: 'rgba(0, 0, 0, 0.8)',
			  titleColor: 'white',
			  bodyColor: 'white',
			  borderColor: 'rgba(255, 255, 255, 0.1)',
			  borderWidth: 1,
			  cornerRadius: 8
			}
		  }
		}
	  });
	}
  
	function getStatCardClass(type: string): string {
	  const baseClass = "relative overflow-hidden rounded-xl border p-6 transition-all duration-200 hover:shadow-lg hover:scale-105";
	  switch (type) {
		case 'total':
		  return `${baseClass} bg-gradient-to-br from-blue-50 to-indigo-100 border-blue-200`;
		case 'open':
		  return `${baseClass} bg-gradient-to-br from-red-50 to-rose-100 border-red-200`;
		case 'in_progress':
		  return `${baseClass} bg-gradient-to-br from-amber-50 to-yellow-100 border-amber-200`;
		case 'resolved':
		  return `${baseClass} bg-gradient-to-br from-green-50 to-emerald-100 border-green-200`;
		case 'closed':
		  return `${baseClass} bg-gradient-to-br from-gray-50 to-slate-100 border-gray-200`;
		default:
		  return `${baseClass} bg-gradient-to-br from-gray-50 to-slate-100 border-gray-200`;
	  }
	}
  
	function getStatIconColor(type: string): string {
	  switch (type) {
		case 'total':
		  return 'text-blue-600';
		case 'open':
		  return 'text-red-600';
		case 'in_progress':
		  return 'text-amber-600';
		case 'resolved':
		  return 'text-green-600';
		case 'closed':
		  return 'text-gray-600';
		default:
		  return 'text-gray-600';
	  }
	}
  
	function getStatIcon(type: string): string {
	  switch (type) {
		case 'total':
		  return 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z';
		case 'open':
		  return 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z';
		case 'in_progress':
		  return 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z';
		case 'resolved':
		  return 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z';
		case 'closed':
		  return 'M5 13l4 4L19 7';
		default:
		  return '';
	  }
	}
  
	function getWelcomeMessage(): string {
	  const hour = new Date().getHours();
	  if (hour < 12) return 'Good morning';
	  if (hour < 17) return 'Good afternoon';
	  return 'Good evening';
	}
  </script>
  
  <svelte:head>
	<title>Dashboard - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<!-- Welcome Header -->
	<div class="mb-8">
	  <div class="flex items-center justify-between">
		<div>
		  <h1 class="text-3xl font-bold text-gray-900">
			{getWelcomeMessage()}, {user?.name || 'User'}! 👋
		  </h1>
		  <p class="mt-2 text-gray-600">
			Here's an overview of your issue tracking system
		  </p>
		</div>
		<div class="hidden sm:flex items-center space-x-3">
		  <button
			on:click={loadDashboardStats}
			disabled={loading}
			class="inline-flex items-center rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-all duration-200"
		  >
			<svg class="mr-2 h-4 w-4 {loading ? 'animate-spin' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
			  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
			</svg>
			Refresh
		  </button>
		  <a
			href="/issues/create"
			class="inline-flex items-center rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-105"
		  >
			<svg class="mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
			  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
			</svg>
			New Issue
		  </a>
		</div>
	  </div>
	</div>
  
	{#if loading}
	  <!-- Modern Loading State -->
	  <div class="space-y-8">
		<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
		  {#each Array(5) as _}
			<div class="animate-pulse rounded-xl bg-white p-6 shadow-sm">
			  <div class="flex items-center">
				<div class="h-12 w-12 rounded-lg bg-gray-200"></div>
				<div class="ml-5 flex-1">
				  <div class="h-4 w-20 rounded bg-gray-200 mb-2"></div>
				  <div class="h-6 w-12 rounded bg-gray-200"></div>
				</div>
			  </div>
			</div>
		  {/each}
		</div>
		<div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
		  <div class="animate-pulse rounded-xl bg-white p-6 shadow-sm">
			<div class="h-6 w-32 rounded bg-gray-200 mb-4"></div>
			<div class="h-64 rounded bg-gray-200"></div>
		  </div>
		  <div class="animate-pulse rounded-xl bg-white p-6 shadow-sm">
			<div class="h-6 w-24 rounded bg-gray-200 mb-4"></div>
			<div class="space-y-3">
			  {#each Array(5) as _}
				<div class="h-16 rounded bg-gray-200"></div>
			  {/each}
			</div>
		  </div>
		</div>
	  </div>
	{:else if error}
	  <!-- Error State -->
	  <div class="rounded-xl bg-white p-12 text-center shadow-sm">
		<div class="mx-auto h-16 w-16 rounded-full bg-red-100 flex items-center justify-center mb-4">
		  <svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
		  </svg>
		</div>
		<h3 class="text-lg font-medium text-gray-900 mb-2">Error Loading Dashboard</h3>
		<p class="text-gray-600 mb-6">{error}</p>
		<button
		  on:click={loadDashboardStats}
		  class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
		>
		  <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
		  </svg>
		  Try Again
		</button>
	  </div>
	{:else if stats}
	  <!-- Statistics Cards -->
	  <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5 mb-8">
		<!-- Total Issues -->
		<div class="{getStatCardClass('total')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <div class="h-12 w-12 rounded-lg bg-blue-500/10 flex items-center justify-center">
				<svg class="h-6 w-6 {getStatIconColor('total')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('total')}" />
				</svg>
			  </div>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Total Issues</dt>
				<dd class="text-2xl font-bold text-gray-900">{stats.total_issues.toLocaleString()}</dd>
			  </dl>
			</div>
		  </div>
		  <!-- Decorative gradient -->
		  <div class="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 opacity-10"></div>
		</div>
  
		<!-- Open Issues -->
		<div class="{getStatCardClass('open')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <div class="h-12 w-12 rounded-lg bg-red-500/10 flex items-center justify-center">
				<svg class="h-6 w-6 {getStatIconColor('open')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('open')}" />
				</svg>
			  </div>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Open</dt>
				<dd class="text-2xl font-bold text-gray-900">{stats.open_issues}</dd>
			  </dl>
			</div>
		  </div>
		  <div class="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br from-red-400 to-rose-500 opacity-10"></div>
		</div>
  
		<!-- In Progress Issues -->
		<div class="{getStatCardClass('in_progress')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <div class="h-12 w-12 rounded-lg bg-amber-500/10 flex items-center justify-center">
				<svg class="h-6 w-6 {getStatIconColor('in_progress')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('in_progress')}" />
				</svg>
			  </div>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
				<dd class="text-2xl font-bold text-gray-900">{stats.in_progress_issues}</dd>
			  </dl>
			</div>
		  </div>
		  <div class="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br from-amber-400 to-yellow-500 opacity-10"></div>
		</div>
  
		<!-- Resolved Issues -->
		<div class="{getStatCardClass('resolved')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <div class="h-12 w-12 rounded-lg bg-green-500/10 flex items-center justify-center">
				<svg class="h-6 w-6 {getStatIconColor('resolved')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('resolved')}" />
				</svg>
			  </div>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Resolved</dt>
				<dd class="text-2xl font-bold text-gray-900">{stats.resolved_issues}</dd>
			  </dl>
			</div>
		  </div>
		  <div class="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 opacity-10"></div>
		</div>
  
		<!-- Closed Issues -->
		<div class="{getStatCardClass('closed')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <div class="h-12 w-12 rounded-lg bg-gray-500/10 flex items-center justify-center">
				<svg class="h-6 w-6 {getStatIconColor('closed')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('closed')}" />
				</svg>
			  </div>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Closed</dt>
				<dd class="text-2xl font-bold text-gray-900">{stats.closed_issues}</dd>
			  </dl>
			</div>
		  </div>
		  <div class="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br from-gray-400 to-slate-500 opacity-10"></div>
		</div>
	  </div>
  
	  <!-- Charts and Recent Issues -->
	  <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
		<!-- Issues Status Chart -->
		<div class="rounded-xl bg-white shadow-sm ring-1 ring-gray-200/50 overflow-hidden">
		  <div class="border-b border-gray-200/50 bg-gradient-to-r from-gray-50 to-white px-6 py-4">
			<h3 class="text-lg font-semibold text-gray-900">Issues by Status</h3>
			<p class="text-sm text-gray-600">Distribution of issues across different statuses</p>
		  </div>
		  <div class="p-6">
			{#if stats.total_issues > 0}
			  <div class="relative h-64">
				<canvas bind:this={chartCanvas}></canvas>
			  </div>
			{:else}
			  <div class="text-center py-8">
				<div class="mx-auto h-16 w-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
				  <svg class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
				  </svg>
				</div>
				<h3 class="text-lg font-medium text-gray-900 mb-2">No Data Available</h3>
				<p class="text-gray-600 mb-4">Create some issues to see statistics</p>
				<a
				  href="/issues/create"
				  class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 transition-all duration-200"
				>
				  Create Your First Issue
				</a>
			  </div>
			{/if}
		  </div>
		</div>
  
		<!-- Recent Issues -->
		<RecentIssues issues={stats.recent_issues} />
	  </div>
  
	  <!-- Quick Actions -->
	  <div class="mt-8 rounded-xl bg-white shadow-sm ring-1 ring-gray-200/50 overflow-hidden">
		<div class="border-b border-gray-200/50 bg-gradient-to-r from-gray-50 to-white px-6 py-4">
		  <h3 class="text-lg font-semibold text-gray-900">Quick Actions</h3>
		  <p class="text-sm text-gray-600">Common tasks to help you manage issues efficiently</p>
		</div>
		<div class="p-6">
		  <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
			<a
			  href="/issues/create"
			  class="group relative rounded-xl border-2 border-dashed border-gray-300 p-6 text-center hover:border-blue-400 transition-all duration-200 transform hover:scale-105"
			>
			  <div class="mx-auto h-12 w-12 rounded-lg bg-blue-500/10 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors duration-200">
				<svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
				</svg>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">
				  Create Issue
				</h3>
				<p class="mt-2 text-sm text-gray-600">
				  Report a new bug or request a feature
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues"
			  class="group relative rounded-xl border-2 border-dashed border-gray-300 p-6 text-center hover:border-green-400 transition-all duration-200 transform hover:scale-105"
			>
			  <div class="mx-auto h-12 w-12 rounded-lg bg-green-500/10 flex items-center justify-center group-hover:bg-green-500/20 transition-colors duration-200">
				<svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
				</svg>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-semibold text-gray-900 group-hover:text-green-600 transition-colors duration-200">
				  View All Issues
				</h3>
				<p class="mt-2 text-sm text-gray-600">
				  Browse and manage all issues
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues?status=OPEN"
			  class="group relative rounded-xl border-2 border-dashed border-gray-300 p-6 text-center hover:border-red-400 transition-all duration-200 transform hover:scale-105"
			>
			  <div class="mx-auto h-12 w-12 rounded-lg bg-red-500/10 flex items-center justify-center group-hover:bg-red-500/20 transition-colors duration-200">
				<svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
				</svg>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-semibold text-gray-900 group-hover:text-red-600 transition-colors duration-200">
				  Open Issues
				</h3>
				<p class="mt-2 text-sm text-gray-600">
				  View issues that need attention
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues?status=IN_PROGRESS"
			  class="group relative rounded-xl border-2 border-dashed border-gray-300 p-6 text-center hover:border-amber-400 transition-all duration-200 transform hover:scale-105"
			>
			  <div class="mx-auto h-12 w-12 rounded-lg bg-amber-500/10 flex items-center justify-center group-hover:bg-amber-500/20 transition-colors duration-200">
				<svg class="h-6 w-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-semibold text-gray-900 group-hover:text-amber-600 transition-colors duration-200">
				  In Progress
				</h3>
				<p class="mt-2 text-sm text-gray-600">
				  View issues currently being worked on
				</p>
			  </div>
			</a>
		  </div>
		</div>
	  </div>
	{/if}
  </div>