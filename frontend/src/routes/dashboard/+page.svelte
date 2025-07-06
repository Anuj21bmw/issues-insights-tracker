<!-- frontend/src/routes/dashboard/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth';
	import { websocketStore } from '$lib/stores/websocket';
	import { apiClient } from '$lib/api/client';
	import Chart from '$lib/stores/components/Chart.svelte';
	import StatsCard from '$lib/stores/components/StatsCard.svelte';
	import RecentIssues from '$lib/stores/components/RecentIssues.svelte';
	import { toastStore } from '$lib/stores/toast';
	
	interface SeverityData {
	  severity: string;
	  count: number;
	}
	
	interface StatusData {
	  status: string;
	  count: number;
	}
	
	interface ChartDataItem {
	  label: string;
	  value: number;
	  color: string;
	}
	
	interface DashboardData {
	  severity_breakdown: SeverityData[];
	  status_breakdown: StatusData[];
	  total_open: number;
	}
	
	let dashboardData: DashboardData | null = null;
	let loading = true;
	let error = '';
	
	$: user = $authStore.user;
	$: isAuthenticated = $authStore.isAuthenticated;
	
	onMount(() => {
	  if (!isAuthenticated) {
		return; // Will be redirected by layout
	  }
	  
	  loadDashboardData();
	  
	  // Listen for real-time updates
	  const handleIssueUpdate = () => {
		loadDashboardData();
	  };
	  
	  window.addEventListener('issue-created', handleIssueUpdate);
	  window.addEventListener('issue-updated', handleIssueUpdate);
	  window.addEventListener('issue-deleted', handleIssueUpdate);
	  
	  return () => {
		window.removeEventListener('issue-created', handleIssueUpdate);
		window.removeEventListener('issue-updated', handleIssueUpdate);
		window.removeEventListener('issue-deleted', handleIssueUpdate);
	  };
	});
	
	async function loadDashboardData() {
	  try {
		loading = true;
		error = '';
		
		const response = await apiClient.getDashboardStats();
		
		if (response.data) {
		  dashboardData = response.data;
		} else {
		  error = response.error || 'Failed to load dashboard data';
		  toastStore.error(error);
		}
	  } catch (err) {
		error = 'Network error loading dashboard';
		console.error('Dashboard error:', err);
		toastStore.error(error);
	  } finally {
		loading = false;
	  }
	}
	
	// Transform data for charts
	$: severityChartData = dashboardData?.severity_breakdown?.map((item: SeverityData): ChartDataItem => ({
	  label: item.severity,
	  value: item.count,
	  color: getSeverityColor(item.severity)
	})) || [];
	
	$: statusChartData = dashboardData?.status_breakdown?.map((item: StatusData): ChartDataItem => ({
	  label: item.status,
	  value: item.count,
	  color: getStatusColor(item.status)
	})) || [];
	
	function getSeverityColor(severity: string): string {
	  switch (severity) {
		case 'LOW': return '#10B981';
		case 'MEDIUM': return '#F59E0B';
		case 'HIGH': return '#EF4444';
		case 'CRITICAL': return '#DC2626';
		default: return '#6B7280';
	  }
	}
	
	function getStatusColor(status: string): string {
	  switch (status) {
		case 'OPEN': return '#EF4444';
		case 'TRIAGED': return '#F59E0B';
		case 'IN_PROGRESS': return '#3B82F6';
		case 'DONE': return '#10B981';
		default: return '#6B7280';
	  }
	}
	
	function findChartValue(data: ChartDataItem[], label: string): number {
	  return data.find((item: ChartDataItem) => item.label === label)?.value || 0;
	}
  </script>
  
  <svelte:head>
	<title>Dashboard - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="space-y-8">
	<!-- Header -->
	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
	  <div class="flex items-center justify-between">
		<div>
		  <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
		  <p class="text-gray-600 dark:text-gray-400 mt-1">
			Welcome back, {user?.role || user?.email}
		  </p>
		  <div class="flex items-center space-x-2 mt-2">
			<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
			  {user?.role}
			</span>
		  </div>
		</div>
		<div class="flex items-center space-x-2">
		  <div class="w-3 h-3 rounded-full {$websocketStore.connected ? 'bg-green-500' : 'bg-red-500'}"></div>
		  <span class="text-sm text-gray-500 dark:text-gray-400">
			{$websocketStore.connected ? 'Real-time updates active' : 'Offline'}
		  </span>
		</div>
	  </div>
	</div>
  
	{#if loading}
	  <div class="flex items-center justify-center py-12">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
		<span class="ml-3 text-gray-600 dark:text-gray-400">Loading dashboard...</span>
	  </div>
	{:else if error}
	  <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
		<div class="flex items-center">
		  <span class="text-red-600 dark:text-red-400 mr-2">❌</span>
		  <span class="text-red-800 dark:text-red-300">{error}</span>
		</div>
		<button 
		  on:click={loadDashboardData}
		  class="mt-2 text-red-700 dark:text-red-300 underline hover:no-underline"
		>
		  Try again
		</button>
	  </div>
	{:else if dashboardData}
	  <!-- Stats Cards -->
	  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		<StatsCard
		  title="Total Open Issues"
		  value={dashboardData.total_open}
		  icon="🐛"
		  trend="neutral"
		  href="/issues?status=OPEN"
		/>
		<StatsCard
		  title="Critical Issues"
		  value={findChartValue(severityChartData, 'CRITICAL')}
		  icon="🚨"
		  trend="warning"
		  href="/issues?severity=CRITICAL"
		/>
		<StatsCard
		  title="In Progress"
		  value={findChartValue(statusChartData, 'IN_PROGRESS')}
		  icon="⚡"
		  trend="info"
		  href="/issues?status=IN_PROGRESS"
		/>
		<StatsCard
		  title="Completed"
		  value={findChartValue(statusChartData, 'DONE')}
		  icon="✅"
		  trend="positive"
		  href="/issues?status=DONE"
		/>
	  </div>
  
	  <!-- Charts Row -->
	  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- Issues by Severity Chart -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
		  <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
			Open Issues by Severity
		  </h2>
		  {#if severityChartData.length > 0}
			<Chart
			  data={severityChartData}
			  type="doughnut"
			  height="300"
			  title="Issues by Severity"
			/>
		  {:else}
			<div class="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
			  <div class="text-center">
				<span class="text-4xl mb-2 block">📊</span>
				<p>No severity data available</p>
				<a href="/issues/create" class="text-blue-600 dark:text-blue-400 hover:underline mt-2 inline-block">
				  Create your first issue
				</a>
			  </div>
			</div>
		  {/if}
		</div>
  
		<!-- Issues by Status Chart -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
		  <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
			Issues by Status
		  </h2>
		  {#if statusChartData.length > 0}
			<Chart
			  data={statusChartData}
			  type="bar"
			  height="300"
			  title="Issues by Status"
			/>
		  {:else}
			<div class="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
			  <div class="text-center">
				<span class="text-4xl mb-2 block">📈</span>
				<p>No status data available</p>
				<a href="/issues/create" class="text-blue-600 dark:text-blue-400 hover:underline mt-2 inline-block">
				  Create your first issue
				</a>
			  </div>
			</div>
		  {/if}
		</div>
	  </div>
  
	  <!-- Recent Issues -->
	  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
		<div class="p-6 border-b border-gray-200 dark:border-gray-700">
		  <div class="flex items-center justify-between">
			<h2 class="text-xl font-semibold text-gray-900 dark:text-white">Recent Issues</h2>
			<a 
			  href="/issues" 
			  class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium"
			>
			  View all →
			</a>
		  </div>
		</div>
		<RecentIssues />
	  </div>
	{:else}
	  <div class="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4">
		<div class="flex items-center">
		  <span class="text-yellow-600 dark:text-yellow-400 mr-2">⚠️</span>
		  <span class="text-yellow-800 dark:text-yellow-300">No dashboard data available</span>
		</div>
		<button 
		  on:click={loadDashboardData}
		  class="mt-2 text-yellow-700 dark:text-yellow-300 underline hover:no-underline"
		>
		  Refresh data
		</button>
	  </div>
	{/if}
  </div>