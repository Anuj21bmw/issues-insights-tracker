<!-- src/routes/dashboard/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import type { DashboardStats } from '$lib/types';
	import RecentIssues from '$lib/stores/components/RecentIssues.svelte';
  
	Chart.register(...registerables);
  
	let stats: DashboardStats | null = null;
	let loading = true;
	let error = '';
	let chartCanvas: HTMLCanvasElement;
	let chart: Chart | null = null;
  
	onMount(async () => {
	  await loadDashboardStats();
	});
  
	async function loadDashboardStats(): Promise<void> {
	  try {
		const token = localStorage.getItem('access_token');
		const response = await fetch('http://localhost:8000/api/dashboard/stats', {
		  headers: {
			'Authorization': `Bearer ${token}`
		  }
		});
  
		if (response.ok) {
		  stats = await response.json();
		  createChart();
		} else {
		  error = 'Failed to load dashboard data';
		}
	  } catch (err) {
		error = 'Network error';
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
  
	  chart = new Chart(ctx, {
		type: 'doughnut',
		data: {
		  labels: ['Open', 'In Progress', 'Resolved', 'Closed'],
		  datasets: [{
			data: [
			  stats.open_issues,
			  stats.in_progress_issues,
			  stats.resolved_issues,
			  stats.closed_issues
			],
			backgroundColor: [
			  '#FEE2E2', // Red for Open
			  '#FEF3C7', // Yellow for In Progress
			  '#D1FAE5', // Green for Resolved
			  '#F3F4F6'  // Gray for Closed
			],
			borderColor: [
			  '#EF4444', // Red
			  '#F59E0B', // Yellow
			  '#10B981', // Green
			  '#6B7280'  // Gray
			],
			borderWidth: 2
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
				  size: 12
				}
			  }
			},
			tooltip: {
			  callbacks: {
				label: function(context) {
				  const label = context.label || '';
				  const value = context.parsed;
				  const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
				  const percentage = ((value / total) * 100).toFixed(1);
				  return `${label}: ${value} (${percentage}%)`;
				}
			  }
			}
		  }
		}
	  });
	}
  
	function getStatCardColor(type: string): string {
	  switch (type) {
		case 'total':
		  return 'bg-blue-50 border-blue-200';
		case 'open':
		  return 'bg-red-50 border-red-200';
		case 'in_progress':
		  return 'bg-yellow-50 border-yellow-200';
		case 'resolved':
		  return 'bg-green-50 border-green-200';
		case 'closed':
		  return 'bg-gray-50 border-gray-200';
		default:
		  return 'bg-gray-50 border-gray-200';
	  }
	}
  
	function getStatIconColor(type: string): string {
	  switch (type) {
		case 'total':
		  return 'text-blue-600';
		case 'open':
		  return 'text-red-600';
		case 'in_progress':
		  return 'text-yellow-600';
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
  </script>
  
  <svelte:head>
	<title>Dashboard - Issue Tracker</title>
  </svelte:head>
  
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
	<!-- Header -->
	<div class="mb-8">
	  <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
	  <p class="mt-2 text-gray-600">Overview of your issue tracking system</p>
	</div>
  
	{#if loading}
	  <div class="animate-pulse">
		<!-- Stats Cards Skeleton -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
		  {#each Array(5) as _}
			<div class="bg-white p-6 rounded-lg border border-gray-200">
			  <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
			  <div class="h-6 bg-gray-200 rounded w-1/2"></div>
			</div>
		  {/each}
		</div>
		
		<!-- Chart and Recent Issues Skeleton -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		  <div class="bg-white p-6 rounded-lg border border-gray-200">
			<div class="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
			<div class="h-64 bg-gray-200 rounded"></div>
		  </div>
		  <div class="bg-white p-6 rounded-lg border border-gray-200">
			<div class="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
			<div class="space-y-3">
			  {#each Array(3) as _}
				<div class="h-4 bg-gray-200 rounded"></div>
			  {/each}
			</div>
		  </div>
		</div>
	  </div>
	{:else if error}
	  <div class="text-center py-12">
		<svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
		  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
		</svg>
		<h3 class="mt-2 text-sm font-medium text-gray-900">Error Loading Dashboard</h3>
		<p class="mt-1 text-sm text-gray-500">{error}</p>
		<div class="mt-6">
		  <button 
			on:click={loadDashboardStats}
			class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
		  >
			Retry
		  </button>
		</div>
	  </div>
	{:else if stats}
	  <!-- Statistics Cards -->
	  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
		<!-- Total Issues -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 {getStatCardColor('total')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <svg class="h-8 w-8 {getStatIconColor('total')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('total')}" />
			  </svg>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Total Issues</dt>
				<dd class="text-lg font-medium text-gray-900">{stats.total_issues}</dd>
			  </dl>
			</div>
		  </div>
		</div>
  
		<!-- Open Issues -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 {getStatCardColor('open')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <svg class="h-8 w-8 {getStatIconColor('open')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('open')}" />
			  </svg>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Open</dt>
				<dd class="text-lg font-medium text-gray-900">{stats.open_issues}</dd>
			  </dl>
			</div>
		  </div>
		</div>
  
		<!-- In Progress Issues -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 {getStatCardColor('in_progress')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <svg class="h-8 w-8 {getStatIconColor('in_progress')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('in_progress')}" />
			  </svg>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
				<dd class="text-lg font-medium text-gray-900">{stats.in_progress_issues}</dd>
			  </dl>
			</div>
		  </div>
		</div>
  
		<!-- Resolved Issues -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 {getStatCardColor('resolved')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <svg class="h-8 w-8 {getStatIconColor('resolved')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('resolved')}" />
			  </svg>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Resolved</dt>
				<dd class="text-lg font-medium text-gray-900">{stats.resolved_issues}</dd>
			  </dl>
			</div>
		  </div>
		</div>
  
		<!-- Closed Issues -->
		<div class="bg-white rounded-lg border border-gray-200 p-6 {getStatCardColor('closed')}">
		  <div class="flex items-center">
			<div class="flex-shrink-0">
			  <svg class="h-8 w-8 {getStatIconColor('closed')}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatIcon('closed')}" />
			  </svg>
			</div>
			<div class="ml-5 w-0 flex-1">
			  <dl>
				<dt class="text-sm font-medium text-gray-500 truncate">Closed</dt>
				<dd class="text-lg font-medium text-gray-900">{stats.closed_issues}</dd>
			  </dl>
			</div>
		  </div>
		</div>
	  </div>
  
	  <!-- Charts and Recent Issues -->
	  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		<!-- Issues Status Chart -->
		<div class="bg-white shadow rounded-lg">
		  <div class="px-6 py-4 border-b border-gray-200">
			<h3 class="text-lg font-medium text-gray-900">Issues by Status</h3>
		  </div>
		  <div class="p-6">
			{#if stats.total_issues > 0}
			  <div class="relative h-64">
				<canvas bind:this={chartCanvas}></canvas>
			  </div>
			{:else}
			  <div class="text-center py-8">
				<svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
				</svg>
				<h3 class="mt-2 text-sm font-medium text-gray-900">No Data</h3>
				<p class="mt-1 text-sm text-gray-500">Create some issues to see statistics</p>
			  </div>
			{/if}
		  </div>
		</div>
  
		<!-- Recent Issues -->
		<RecentIssues issues={stats.recent_issues} />
	  </div>
  
	  <!-- Quick Actions -->
	  <div class="mt-8 bg-white shadow rounded-lg">
		<div class="px-6 py-4 border-b border-gray-200">
		  <h3 class="text-lg font-medium text-gray-900">Quick Actions</h3>
		</div>
		<div class="p-6">
		  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
			<a
			  href="/issues/new"
			  class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
			>
			  <div>
				<span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-600 group-hover:bg-blue-100">
				  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
				  </svg>
				</span>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-medium">
				  <span class="absolute inset-0" aria-hidden="true"></span>
				  Create Issue
				</h3>
				<p class="mt-2 text-sm text-gray-500">
				  Report a new bug or request a feature
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues"
			  class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
			>
			  <div>
				<span class="rounded-lg inline-flex p-3 bg-green-50 text-green-600 group-hover:bg-green-100">
				  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
				  </svg>
				</span>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-medium">
				  <span class="absolute inset-0" aria-hidden="true"></span>
				  View All Issues
				</h3>
				<p class="mt-2 text-sm text-gray-500">
				  Browse and manage all issues
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues?status=OPEN"
			  class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
			>
			  <div>
				<span class="rounded-lg inline-flex p-3 bg-red-50 text-red-600 group-hover:bg-red-100">
				  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
				  </svg>
				</span>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-medium">
				  <span class="absolute inset-0" aria-hidden="true"></span>
				  Open Issues
				</h3>
				<p class="mt-2 text-sm text-gray-500">
				  View issues that need attention
				</p>
			  </div>
			</a>
  
			<a
			  href="/issues?status=IN_PROGRESS"
			  class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
			>
			  <div>
				<span class="rounded-lg inline-flex p-3 bg-yellow-50 text-yellow-600 group-hover:bg-yellow-100">
				  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
				  </svg>
				</span>
			  </div>
			  <div class="mt-4">
				<h3 class="text-lg font-medium">
				  <span class="absolute inset-0" aria-hidden="true"></span>
				  In Progress
				</h3>
				<p class="mt-2 text-sm text-gray-500">
				  View issues currently being worked on
				</p>
			  </div>
			</a>
		  </div>
		</div>
	  </div>
	{/if}
  </div>