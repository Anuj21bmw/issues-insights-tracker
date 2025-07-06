<!-- src/routes/issues/+page.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { Issue, IssueStatus } from '$lib/types';
    import { authStore } from '$lib/stores/auth';
    import { toastStore } from '$lib/stores/toast';
  
    let issues: Issue[] = [];
    let loading = true;
    let error = '';
    let searchQuery = '';
    let statusFilter: IssueStatus | 'ALL' = 'ALL';
    let currentPage = 1;
    let totalPages = 1;
    let totalIssues = 0;
  
    $: filteredIssues = issues.filter(issue => {
      const matchesSearch = issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           (issue.description && issue.description.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesStatus = statusFilter === 'ALL' || issue.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  
    onMount(() => {
      // Get status filter from URL params
      const urlParams = new URLSearchParams($page.url.search);
      const status = urlParams.get('status');
      if (status && ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'].includes(status)) {
        statusFilter = status as IssueStatus;
      }
      
      loadIssues();
    });
  
    async function loadIssues(): Promise<void> {
      try {
        loading = true;
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          error = 'Not authenticated';
          return;
        }
  
        const response = await fetch('http://localhost:8000/api/issues/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (response.ok) {
          issues = await response.json();
          totalIssues = issues.length;
          totalPages = Math.ceil(totalIssues / 10); // Assuming 10 items per page
        } else {
          error = 'Failed to load issues';
          toastStore.add({
            type: 'error',
            title: 'Load Failed',
            message: 'Failed to load issues'
          });
        }
      } catch (err) {
        error = 'Network error';
        toastStore.add({
          type: 'error',
          title: 'Network Error',
          message: 'Failed to load issues'
        });
      } finally {
        loading = false;
      }
    }
  
    function getStatusColor(status: IssueStatus): string {
      switch (status) {
        case 'OPEN':
          return 'bg-red-100 text-red-800 border-red-200';
        case 'IN_PROGRESS':
          return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        case 'RESOLVED':
          return 'bg-green-100 text-green-800 border-green-200';
        case 'CLOSED':
          return 'bg-gray-100 text-gray-800 border-gray-200';
        default:
          return 'bg-gray-100 text-gray-800 border-gray-200';
      }
    }
  
    function formatDate(dateString: string): string {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  
    function getStatusIcon(status: IssueStatus): string {
      switch (status) {
        case 'OPEN':
          return 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z';
        case 'IN_PROGRESS':
          return 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z';
        case 'RESOLVED':
          return 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z';
        case 'CLOSED':
          return 'M5 13l4 4L19 7';
        default:
          return '';
      }
    }
  </script>
  
  <svelte:head>
    <title>Issues - Issue Tracker</title>
  </svelte:head>
  
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Issues
          </h1>
          <p class="mt-1 text-sm text-gray-500">
            {totalIssues} total issues
          </p>
        </div>
        <div class="mt-4 flex md:mt-0 md:ml-4">
          <a
            href="/issues/new"
            class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="-ml-1 mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            New Issue
          </a>
        </div>
      </div>
    </div>
  
    <!-- Filters and Search -->
    <div class="mb-6">
      <div class="bg-white shadow rounded-lg p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Search -->
          <div>
            <label for="search" class="block text-sm font-medium text-gray-700">Search</label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                id="search"
                type="text"
                bind:value={searchQuery}
                placeholder="Search issues..."
                class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>
  
          <!-- Status Filter -->
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
            <select
              id="status"
              bind:value={statusFilter}
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="ALL">All Statuses</option>
              <option value="OPEN">Open</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="RESOLVED">Resolved</option>
              <option value="CLOSED">Closed</option>
            </select>
          </div>
  
          <!-- Refresh Button -->
          <div class="flex items-end">
            <button
              on:click={loadIssues}
              disabled={loading}
              class="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Issues List -->
    {#if loading}
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4">
          <div class="animate-pulse space-y-4">
            {#each Array(5) as _}
              <div class="flex items-center space-x-4">
                <div class="h-4 bg-gray-200 rounded w-1/4"></div>
                <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                <div class="h-6 bg-gray-200 rounded w-20"></div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    {:else if error}
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-12 text-center">
          <svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Error Loading Issues</h3>
          <p class="mt-1 text-sm text-gray-500">{error}</p>
          <div class="mt-6">
            <button
              on:click={loadIssues}
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    {:else if filteredIssues.length === 0}
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-12 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No issues found</h3>
          <p class="mt-1 text-sm text-gray-500">
            {searchQuery || statusFilter !== 'ALL' 
              ? 'Try adjusting your search or filter criteria.' 
              : 'Get started by creating your first issue.'}
          </p>
          <div class="mt-6">
            <a
              href="/issues/new"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              Create Issue
            </a>
          </div>
        </div>
      </div>
    {:else}
      <div class="bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          {#each filteredIssues as issue}
            <li>
              <a href="/issues/{issue.id}" class="block hover:bg-gray-50 transition-colors">
                <div class="px-4 py-4 sm:px-6">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0 flex-1">
                      <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{getStatusIcon(issue.status)}" />
                        </svg>
                      </div>
                      <div class="ml-4 flex-1 min-w-0">
                        <div class="flex items-center space-x-3">
                          <p class="text-sm font-medium text-gray-900 truncate">
                            {issue.title}
                          </p>
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {getStatusColor(issue.status)}">
                            {issue.status.replace('_', ' ')}
                          </span>
                          {#if issue.severity}
                            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium border bg-gray-50 text-gray-700 border-gray-200">
                              {issue.severity}
                            </span>
                          {/if}
                        </div>
                        <div class="mt-2 sm:flex sm:justify-between">
                          <div class="sm:flex">
                            <p class="flex items-center text-sm text-gray-500">
                              <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              Created {formatDate(issue.created_at)}
                            </p>
                            {#if issue.created_by}
                              <p class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                                <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                by {issue.created_by}
                              </p>
                            {/if}
                          </div>
                        </div>
                        {#if issue.description}
                          <p class="mt-2 text-sm text-gray-500 line-clamp-2">
                            {issue.description}
                          </p>
                        {/if}
                      </div>
                    </div>
                    <div class="ml-5 flex-shrink-0">
                      <svg class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>
              </a>
            </li>
          {/each}
        </ul>
      </div>
  
      <!-- Pagination (if needed) -->
      {#if totalPages > 1}
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-6 rounded-lg shadow">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              disabled={currentPage === 1}
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <button
              disabled={currentPage === totalPages}
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing <span class="font-medium">1</span> to <span class="font-medium">{Math.min(10, filteredIssues.length)}</span> of{' '}
                <span class="font-medium">{filteredIssues.length}</span> results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  disabled={currentPage === 1}
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <span class="sr-only">Previous</span>
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                
                {#each Array(Math.min(5, totalPages)) as _, i}
                  <button
                    class="relative inline-flex items-center px-4 py-2 border text-sm font-medium {i + 1 === currentPage ? 'z-10 bg-blue-50 border-blue-500 text-blue-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'}"
                  >
                    {i + 1}
                  </button>
                {/each}
                
                <button
                  disabled={currentPage === totalPages}
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <span class="sr-only">Next</span>
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>