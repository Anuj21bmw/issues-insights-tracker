<!-- src/routes/issues/[id]/+page.svelte -->
<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import type { Issue, IssueStatus } from '$lib/types';
    import { toasts } from '$lib/stores/toast';
  
    let issue: Issue | null = null;
    let loading = true;
    let error = '';
    let updating = false;
  
    $: issueId = $page.params.id;
  
    onMount(() => {
      loadIssue();
    });
  
    async function loadIssue(): Promise<void> {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`http://localhost:8000/api/issues/${issueId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (response.ok) {
          issue = await response.json();
        } else {
          error = 'Issue not found';
        }
      } catch (err) {
        error = 'Failed to load issue';
      } finally {
        loading = false;
      }
    }
  
    async function updateStatus(newStatus: IssueStatus): Promise<void> {
      if (!issue) return;
      
      updating = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`http://localhost:8000/api/issues/${issueId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            title: issue.title,
            description: issue.description,
            status: newStatus
          })
        });
  
        if (response.ok) {
          issue = await response.json();
          toasts.success('Status Updated', `Issue status changed to ${newStatus.replace('_', ' ')}`);
        } else {
          toasts.error('Update Failed', 'Failed to update issue status');
        }
      } catch (err) {
        toasts.error('Network Error', 'Failed to update issue status');
      } finally {
        updating = false;
      }
    }
  
    async function deleteIssue(): Promise<void> {
      if (!confirm('Are you sure you want to delete this issue?')) return;
      
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`http://localhost:8000/api/issues/${issueId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (response.ok) {
          toasts.success('Issue Deleted', 'Issue has been deleted successfully');
          goto('/issues');
        } else {
          toasts.error('Delete Failed', 'Failed to delete issue');
        }
      } catch (err) {
        toasts.error('Network Error', 'Failed to delete issue');
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
  
    function getStatusIcon(status: IssueStatus): string {
      switch (status) {
        case 'OPEN':
          return 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z';
        case 'IN_PROGRESS':
          return 'M10 18a8 8 0 100-16 8 8 0 000 16zm-1-4a1 1 0 112 0v-4a1 1 0 11-2 0v4zm0-8a1 1 0 112 0 1 1 0 01-2 0z';
        case 'RESOLVED':
          return 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z';
        case 'CLOSED':
          return 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z';
        default:
          return '';
      }
    }
  
    function getAvailableStatuses(currentStatus: IssueStatus): IssueStatus[] {
      const allStatuses: IssueStatus[] = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'];
      return allStatuses.filter(status => status !== currentStatus);
    }
  
    function formatDate(dateString: string): string {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  </script>
  
  <svelte:head>
    <title>{issue ? `${issue.title} - Issue Tracker` : 'Loading - Issue Tracker'}</title>
  </svelte:head>
  
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    {#if loading}
      <div class="animate-pulse">
        <div class="mb-8">
          <div class="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div class="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div class="bg-white shadow rounded-lg p-6">
          <div class="space-y-4">
            <div class="h-4 bg-gray-200 rounded w-full"></div>
            <div class="h-4 bg-gray-200 rounded w-5/6"></div>
            <div class="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    {:else if error}
      <div class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">Error</h3>
        <p class="mt-1 text-sm text-gray-500">{error}</p>
        <div class="mt-6">
          <a href="/issues" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
            Back to Issues
          </a>
        </div>
      </div>
    {:else if issue}
      <!-- Breadcrumb -->
      <nav class="flex mb-8" aria-label="Breadcrumb">
        <ol class="flex items-center space-x-4">
          <li>
            <div>
              <a href="/issues" class="text-gray-400 hover:text-gray-500">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only">Back</span>
              </a>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <a href="/issues" class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">Issues</a>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <span class="ml-4 text-sm font-medium text-gray-500">#{issue.id.slice(0, 8)}</span>
            </div>
          </li>
        </ol>
      </nav>
  
      <!-- Issue Header -->
      <div class="mb-8">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-gray-900 mb-2">{issue.title}</h1>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>Created {formatDate(issue.created_at)}</span>
              <span>•</span>
              <span>ID: {issue.id.slice(0, 8)}</span>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border {getStatusColor(issue.status)}">
              <svg class="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="{getStatusIcon(issue.status)}" clip-rule="evenodd" />
              </svg>
              {issue.status.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>
  
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2">
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Description</h3>
            </div>
            <div class="px-6 py-4">
              {#if issue.description}
                <div class="prose max-w-none text-gray-700 whitespace-pre-wrap">
                  {issue.description}
                </div>
              {:else}
                <p class="text-gray-500 italic">No description provided.</p>
              {/if}
            </div>
          </div>
        </div>
  
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Actions -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Actions</h3>
              
              <div class="space-y-3">
                <a
                  href="/issues/{issue.id}/edit"
                  class="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit Issue
                </a>
  
                <button
                  on:click={deleteIssue}
                  class="w-full inline-flex items-center justify-center px-4 py-2 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete Issue
                </button>
              </div>
            </div>
          </div>
  
          <!-- Status Change -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Change Status</h3>
              
              <div class="space-y-2">
                {#each getAvailableStatuses(issue.status) as status}
                  <button
                    on:click={() => updateStatus(status)}
                    disabled={updating}
                    class="w-full text-left px-3 py-2 text-sm rounded-md border border-gray-200 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <div class="flex items-center">
                      <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium {getStatusColor(status)}">
                        {status.replace('_', ' ')}
                      </span>
                    </div>
                  </button>
                {/each}
              </div>
            </div>
          </div>
  
          <!-- Metadata -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Details</h3>
              
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Status</dt>
                  <dd class="mt-1">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(issue.status)}">
                      {issue.status.replace('_', ' ')}
                    </span>
                  </dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Created</dt>
                  <dd class="mt-1 text-sm text-gray-900">{formatDate(issue.created_at)}</dd>
                </div>
  
                {#if issue.updated_at && issue.updated_at !== issue.created_at}
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Last Updated</dt>
                    <dd class="mt-1 text-sm text-gray-900">{formatDate(issue.updated_at)}</dd>
                  </div>
                {/if}
  
                <div>
                  <dt class="text-sm font-medium text-gray-500">Issue ID</dt>
                  <dd class="mt-1 text-sm text-gray-900 font-mono">{issue.id}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>