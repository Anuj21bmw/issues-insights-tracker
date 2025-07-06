<!-- frontend/src/lib/components/RecentIssues.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    
    interface Issue {
      id: string;
      title: string;
      description?: string;
      status: 'OPEN' | 'TRIAGED' | 'IN_PROGRESS' | 'DONE';
      severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
      created_at: string;
      updated_at: string;
      created_by: string;
      assigned_to?: string;
      tags?: string;
    }
    
    let issues: Issue[] = [];
    let loading = true;
    let error = '';
    
    $: token = $authStore.token;
    
    onMount(() => {
      loadRecentIssues();
      
      // Listen for real-time updates
      const handleIssueUpdate = () => {
        loadRecentIssues();
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
    
    async function loadRecentIssues() {
      if (!token) return;
      
      try {
        loading = true;
        error = '';
        
        const response = await fetch('http://localhost:8000/api/issues?limit=10', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          issues = Array.isArray(data) ? data.slice(0, 10) : [];
        } else {
          error = 'Failed to load recent issues';
        }
      } catch (err) {
        error = 'Network error loading issues';
        console.error('Recent issues error:', err);
      } finally {
        loading = false;
      }
    }
    
    function getStatusColor(status: Issue['status']): string {
      switch (status) {
        case 'OPEN': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
        case 'TRIAGED': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
        case 'IN_PROGRESS': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
        case 'DONE': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
        default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
      }
    }
    
    function getSeverityColor(severity: Issue['severity']): string {
      switch (severity) {
        case 'LOW': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
        case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
        case 'HIGH': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
        case 'CRITICAL': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
        default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
      }
    }
    
    function formatDate(dateString: string): string {
      const date = new Date(dateString);
      const now = new Date();
      const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
      
      if (diffInHours < 1) {
        return 'Just now';
      } else if (diffInHours < 24) {
        return `${diffInHours}h ago`;
      } else {
        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays}d ago`;
      }
    }
    
    function viewIssue(issueId: string) {
      goto(`/issues/${issueId}`);
    }
    
    function truncateText(text: string, maxLength: number = 100): string {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    }
  </script>
  
  <div class="p-6">
    {#if loading}
      <div class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-2 text-gray-600 dark:text-gray-400">Loading recent issues...</span>
      </div>
    {:else if error}
      <div class="text-center py-8">
        <div class="text-red-600 dark:text-red-400 mb-2">❌ {error}</div>
        <button 
          on:click={loadRecentIssues}
          class="text-blue-600 dark:text-blue-400 hover:underline"
        >
          Try again
        </button>
      </div>
    {:else if issues.length === 0}
      <div class="text-center py-8">
        <div class="text-gray-500 dark:text-gray-400 mb-4">
          <span class="text-4xl">📝</span>
        </div>
        <p class="text-gray-600 dark:text-gray-400">No issues found</p>
        <button 
          on:click={() => goto('/issues/create')}
          class="mt-2 text-blue-600 dark:text-blue-400 hover:underline"
        >
          Create your first issue
        </button>
      </div>
    {:else}
      <div class="space-y-3">
        {#each issues as issue (issue.id)}
          <div 
            class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-750 cursor-pointer transition-colors duration-200"
            on:click={() => viewIssue(issue.id)}
            on:keydown={(e) => e.key === 'Enter' && viewIssue(issue.id)}
            role="button"
            tabindex="0"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-2">
                  <h3 class="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {issue.title}
                  </h3>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getStatusColor(issue.status)}">
                    {issue.status}
                  </span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getSeverityColor(issue.severity)}">
                    {issue.severity}
                  </span>
                </div>
                
                {#if issue.description}
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {truncateText(issue.description)}
                  </p>
                {/if}
                
                <div class="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                  <span>{formatDate(issue.created_at)}</span>
                  {#if issue.tags}
                    <span class="flex items-center">
                      <span class="mr-1">🏷️</span>
                      {issue.tags.split(',').slice(0, 2).join(', ')}
                      {#if issue.tags.split(',').length > 2}
                        <span class="ml-1">+{issue.tags.split(',').length - 2}</span>
                      {/if}
                    </span>
                  {/if}
                </div>
              </div>
              
              <div class="flex-shrink-0 ml-4">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </div>
        {/each}
      </div>
      
      <div class="mt-6 text-center">
        <button 
          on:click={() => goto('/issues')}
          class="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 font-medium"
        >
          View all issues →
        </button>
      </div>
    {/if}
  </div>