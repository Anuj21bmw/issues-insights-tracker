<!-- src/routes/issues/+page.svelte - Fixed CSS line-clamp issue -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '$lib/stores/auth';
    import { toastStore } from '$lib/stores/toast';
    import { apiClient } from '$lib/api/client';
    import { goto } from '$app/navigation';
    import type { Issue } from '$lib/types';
    
    let issues: Issue[] = [];
    let loading = true;
    let searchTerm = '';
    let statusFilter: string = 'all';
    let sortBy: 'created_at' | 'title' | 'status' = 'created_at';
    let sortOrder: 'asc' | 'desc' = 'desc';
    
    $: isAuthenticated = $authStore.isAuthenticated;
    $: user = $authStore.user;
    
    // Filtered and sorted issues
    $: filteredIssues = issues
      .filter(issue => {
        const matchesSearch = issue.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                             (issue.description && issue.description.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesStatus = statusFilter === 'all' || issue.status === statusFilter;
        return matchesSearch && matchesStatus;
      })
      .sort((a, b) => {
        let comparison = 0;
        if (sortBy === 'created_at') {
          comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        } else if (sortBy === 'title') {
          comparison = a.title.localeCompare(b.title);
        } else if (sortBy === 'status') {
          comparison = a.status.localeCompare(b.status);
        }
        return sortOrder === 'desc' ? -comparison : comparison;
      });
    
    onMount(async () => {
      if (!isAuthenticated) {
        goto('/auth/login');
        return;
      }
      
      await loadIssues();
    });
    
    async function loadIssues() {
      try {
        loading = true;
        const response = await apiClient.getIssues();
        
        if (response.data) {
          issues = response.data;
        } else {
          toastStore.error(response.error || 'Failed to load issues');
        }
      } catch (error) {
        console.error('Load issues error:', error);
        toastStore.error('Network error. Please try again.');
      } finally {
        loading = false;
      }
    }
    
    function getStatusColor(status: string): string {
      switch (status) {
        case 'OPEN': return 'bg-green-100 text-green-800';
        case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800';
        case 'RESOLVED': return 'bg-blue-100 text-blue-800';
        case 'CLOSED': return 'bg-gray-100 text-gray-800';
        default: return 'bg-gray-100 text-gray-800';
      }
    }
    
    function getStatusIcon(status: string): string {
      switch (status) {
        case 'OPEN': return '🟢';
        case 'IN_PROGRESS': return '🟡';
        case 'RESOLVED': return '🔵';
        case 'CLOSED': return '⚫';
        default: return '⚪';
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
    
    function toggleSort(field: typeof sortBy) {
      if (sortBy === field) {
        sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        sortBy = field;
        sortOrder = 'desc';
      }
    }
    
    function handleCreateIssue() {
      goto('/issues/create');
    }
    
    function handleIssueClick(issue: Issue) {
      goto(`/issues/${issue.id}`);
    }
  </script>
  
  <svelte:head>
    <title>Issues - Issue Tracker</title>
  </svelte:head>
  
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Issues</h1>
            <p class="mt-2 text-gray-600">
              Track and manage project issues and feature requests
            </p>
          </div>
          <button
            type="button"
            on:click={handleCreateIssue}
            class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            New Issue
          </button>
        </div>
      </div>
  
      <!-- Filters and Search -->
      <div class="mb-6 rounded-lg bg-white p-6 shadow-sm ring-1 ring-gray-200">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <!-- Search -->
          <div>
            <label for="search" class="block text-sm font-medium text-gray-700 mb-1">
              Search Issues
            </label>
            <div class="relative">
              <input
                type="text"
                id="search"
                bind:value={searchTerm}
                placeholder="Search by title or description..."
                class="block w-full rounded-lg border-gray-300 pl-10 pr-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
              <div class="absolute inset-y-0 left-0 flex items-center pl-3">
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>
  
          <!-- Status Filter -->
          <div>
            <label for="status-filter" class="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="status-filter"
              bind:value={statusFilter}
              class="block w-full rounded-lg border-gray-300 py-2 pl-3 pr-10 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            >
              <option value="all">All Statuses</option>
              <option value="OPEN">Open</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="RESOLVED">Resolved</option>
              <option value="CLOSED">Closed</option>
            </select>
          </div>
  
          <!-- Sort -->
          <div>
            <label for="sort" class="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <select
              id="sort"
              bind:value={sortBy}
              class="block w-full rounded-lg border-gray-300 py-2 pl-3 pr-10 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            >
              <option value="created_at">Date Created</option>
              <option value="title">Title</option>
              <option value="status">Status</option>
            </select>
          </div>
        </div>
  
        <!-- Stats -->
        <div class="mt-4 flex items-center justify-between border-t border-gray-200 pt-4">
          <div class="flex items-center space-x-4 text-sm text-gray-600">
            <span>Total: {issues.length}</span>
            <span>Filtered: {filteredIssues.length}</span>
          </div>
          <button
            type="button"
            on:click={() => sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'}
            class="flex items-center text-sm text-gray-600 hover:text-gray-900"
          >
            Sort {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>
      </div>
  
      <!-- Issues List -->
      {#if loading}
        <div class="flex items-center justify-center py-12">
          <div class="text-center">
            <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
            <p class="mt-4 text-gray-600">Loading issues...</p>
          </div>
        </div>
      {:else if filteredIssues.length === 0}
        <div class="rounded-lg bg-white p-12 shadow-sm ring-1 ring-gray-200 text-center">
          {#if issues.length === 0}
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No issues yet</h3>
            <p class="mt-2 text-gray-600">Get started by creating your first issue.</p>
            <button
              type="button"
              on:click={handleCreateIssue}
              class="mt-4 inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700"
            >
              Create Issue
            </button>
          {:else}
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No issues found</h3>
            <p class="mt-2 text-gray-600">Try adjusting your search or filter criteria.</p>
          {/if}
        </div>
      {:else}
        <div class="space-y-4">
          {#each filteredIssues as issue (issue.id)}
            <div
              class="rounded-lg bg-white p-6 shadow-sm ring-1 ring-gray-200 hover:shadow-md transition-shadow cursor-pointer"
              on:click={() => handleIssueClick(issue)}
              role="button"
              tabindex="0"
              on:keydown={(e) => e.key === 'Enter' && handleIssueClick(issue)}
            >
              <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-lg font-medium text-gray-900 truncate">
                      {issue.title}
                    </h3>
                    <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {getStatusColor(issue.status)}">
                      <span class="mr-1">{getStatusIcon(issue.status)}</span>
                      {issue.status.replace('_', ' ')}
                    </span>
                  </div>
                  
                  {#if issue.description}
                    <p class="mt-2 text-sm text-gray-600 description-clamp">
                      {issue.description}
                    </p>
                  {/if}
                  
                  <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                    <span>#{issue.id.slice(0, 8)}</span>
                    <span>Created {formatDate(issue.created_at)}</span>
                    {#if issue.creator}
                      <span>by {issue.creator.email}</span>
                    {/if}
                  </div>
                </div>
                
                <div class="ml-4 flex-shrink-0">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          {/each}
        </div>
  
        <!-- Pagination (if needed later) -->
        {#if filteredIssues.length > 0}
          <div class="mt-8 flex items-center justify-center">
            <p class="text-sm text-gray-700">
              Showing {filteredIssues.length} of {issues.length} issues
            </p>
          </div>
        {/if}
      {/if}
    </div>
  </div>
  
  <style>
    .description-clamp {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>