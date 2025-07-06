<!-- src/lib/stores/components/RecentIssues.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import type { Issue } from '$lib/types';
  
    export let issues: Issue[] = [];
    
    let loading = true;
    let error = '';
  
    onMount(async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:8000/issues/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          issues = data.slice(0, 5); // Show only recent 5 issues
        } else {
          error = 'Failed to load issues';
        }
      } catch (err) {
        error = 'Network error';
      } finally {
        loading = false;
      }
    });
  
    function getStatusColor(status: Issue['status']): string {
      switch (status) {
        case 'OPEN':
          return 'bg-red-100 text-red-800';
        case 'IN_PROGRESS':
          return 'bg-yellow-100 text-yellow-800';
        case 'RESOLVED':
          return 'bg-green-100 text-green-800';
        case 'CLOSED':
          return 'bg-gray-100 text-gray-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    }
  
    function getSeverityColor(severity: Issue['severity']): string {
      switch (severity) {
        case 'CRITICAL':
          return 'bg-red-100 text-red-800 border-red-200';
        case 'HIGH':
          return 'bg-orange-100 text-orange-800 border-orange-200';
        case 'MEDIUM':
          return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        case 'LOW':
          return 'bg-green-100 text-green-800 border-green-200';
        default:
          return 'bg-gray-100 text-gray-800 border-gray-200';
      }
    }
  
    function formatDate(dateString: string): string {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  </script>
  
  <div class="bg-white shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Issues</h3>
      
      {#if loading}
        <div class="animate-pulse space-y-3">
          {#each Array(3) as _}
            <div class="flex items-center space-x-3">
              <div class="h-4 bg-gray-200 rounded w-1/4"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
              <div class="h-6 bg-gray-200 rounded w-16"></div>
            </div>
          {/each}
        </div>
      {:else if error}
        <div class="text-red-600 text-sm">{error}</div>
      {:else if issues.length === 0}
        <div class="text-center py-6">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No issues</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new issue.</p>
          <div class="mt-6">
            <a
              href="/issues/new"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              New Issue
            </a>
          </div>
        </div>
      {:else}
        <div class="space-y-3">
          {#each issues as issue}
            <div class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-3">
                  <a 
                    href="/issues/{issue.id}" 
                    class="text-sm font-medium text-gray-900 hover:text-blue-600 truncate"
                  >
                    {issue.title}
                  </a>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(issue.status)}">
                    {issue.status.replace('_', ' ')}
                  </span>
                  {#if issue.severity}
                    <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium border {getSeverityColor(issue.severity)}">
                      {issue.severity}
                    </span>
                  {/if}
                </div>
                <p class="mt-1 text-sm text-gray-500 truncate">
                  Created {formatDate(issue.created_at)}
                </p>
              </div>
              <div class="flex-shrink-0">
                <a 
                  href="/issues/{issue.id}" 
                  class="text-blue-600 hover:text-blue-500 text-sm font-medium"
                >
                  View
                </a>
              </div>
            </div>
          {/each}
        </div>
        
        <div class="mt-4">
          <a
            href="/issues"
            class="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            View all issues →
          </a>
        </div>
      {/if}
    </div>
  </div>