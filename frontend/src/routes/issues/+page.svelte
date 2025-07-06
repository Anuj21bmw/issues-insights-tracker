<!-- frontend/src/routes/issues/+page.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '$lib/stores/auth';
    import { websocketStore } from '$lib/stores/websocket';
    import { toastStore } from '$lib/stores/toast';
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
      file_path?: string;
    }
    
    let issues: Issue[] = [];
    let filteredIssues: Issue[] = [];
    let loading = true;
    let error = '';
    
    // Filters
    let statusFilter = '';
    let severityFilter = '';
    let searchQuery = '';
    
    $: user = $authStore.user;
    $: token = $authStore.token;
    
    // Apply filters
    $: {
      filteredIssues = issues.filter(issue => {
        const matchesStatus = !statusFilter || issue.status === statusFilter;
        const matchesSeverity = !severityFilter || issue.severity === severityFilter;
        const matchesSearch = !searchQuery || 
          issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          issue.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          issue.tags?.toLowerCase().includes(searchQuery.toLowerCase());
        
        return matchesStatus && matchesSeverity && matchesSearch;
      });
    }
    
    onMount(() => {
      loadIssues();
      
      // Listen for real-time updates
      const handleIssueCreated = (event: CustomEvent) => {
        issues = [event.detail, ...issues];
        toastStore.success('New issue created');
      };
      
      const handleIssueUpdated = (event: CustomEvent) => {
        const updatedIssue = event.detail;
        issues = issues.map(issue => 
          issue.id === updatedIssue.id ? updatedIssue : issue
        );
        toastStore.info('Issue updated');
      };
      
      const handleIssueDeleted = (event: CustomEvent) => {
        const { id } = event.detail;
        issues = issues.filter(issue => issue.id !== id);
        toastStore.warning('Issue deleted');
      };
      
      window.addEventListener('issue-created', handleIssueCreated as EventListener);
      window.addEventListener('issue-updated', handleIssueUpdated as EventListener);
      window.addEventListener('issue-deleted', handleIssueDeleted as EventListener);
      
      return () => {
        window.removeEventListener('issue-created', handleIssueCreated as EventListener);
        window.removeEventListener('issue-updated', handleIssueUpdated as EventListener);
        window.removeEventListener('issue-deleted', handleIssueDeleted as EventListener);
      };
    });
    
    async function loadIssues() {
      if (!token) return;
      
      try {
        loading = true;
        error = '';
        
        const response = await fetch('http://localhost:8000/api/issues', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          issues = await response.json();
        } else {
          error = 'Failed to load issues';
        }
      } catch (err) {
        error = 'Network error loading issues';
        console.error('Issues error:', err);
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
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
    
    function viewIssue(issueId: string) {
      goto(`/issues/${issueId}`);
    }
    
    function createIssue() {
      goto('/issues/create');
    }
    
    function clearFilters() {
      statusFilter = '';
      severityFilter = '';
      searchQuery = '';
    }
    
    function truncateText(text: string, maxLength: number = 120): string {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    }
  </script>
  
  <svelte:head>
    <title>Issues - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Issues</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-1">
          Manage and track all issues
        </p>
      </div>
      
      <button
        on:click={createIssue}
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
      >
        <span class="mr-2">➕</span>
        Create Issue
      </button>
    </div>
    
    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Search -->
        <div>
          <label for="search" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Search
          </label>
          <input
            id="search"
            type="text"
            bind:value={searchQuery}
            placeholder="Search issues..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <!-- Status Filter -->
        <div>
          <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Status
          </label>
          <select
            id="status"
            bind:value={statusFilter}
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="OPEN">Open</option>
            <option value="TRIAGED">Triaged</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="DONE">Done</option>
          </select>
        </div>
        
        <!-- Severity Filter -->
        <div>
          <label for="severity" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Severity
          </label>
          <select
            id="severity"
            bind:value={severityFilter}
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">All Severities</option>
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>
        
        <!-- Clear Filters -->
        <div class="flex items-end">
          <button
            on:click={clearFilters}
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
          >
            Clear Filters
          </button>
        </div>
      </div>
      
      <!-- Filter Summary -->
      {#if statusFilter || severityFilter || searchQuery}
        <div class="mt-4 flex items-center space-x-2">
          <span class="text-sm text-gray-500 dark:text-gray-400">Active filters:</span>
          {#if searchQuery}
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
              Search: {searchQuery}
            </span>
          {/if}
          {#if statusFilter}
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
              Status: {statusFilter}
            </span>
          {/if}
          {#if severityFilter}
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
              Severity: {severityFilter}
            </span>
          {/if}
        </div>
      {/if}
    </div>
    
    <!-- Issues List -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      {#if loading}
        <div class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600 dark:text-gray-400">Loading issues...</span>
        </div>
      {:else if error}
        <div class="text-center py-12">
          <div class="text-red-600 dark:text-red-400 mb-4">
            <span class="text-4xl">❌</span>
          </div>
          <p class="text-red-800 dark:text-red-300 mb-4">{error}</p>
          <button 
            on:click={loadIssues}
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            Try again
          </button>
        </div>
      {:else if filteredIssues.length === 0}
        <div class="text-center py-12">
          <div class="text-gray-400 mb-4">
            <span class="text-6xl">📝</span>
          </div>
          {#if issues.length === 0}
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No issues yet</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Get started by creating your first issue</p>
            <button 
              on:click={createIssue}
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              <span class="mr-2">➕</span>
              Create Issue
            </button>
          {:else}
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No matching issues</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Try adjusting your filters</p>
            <button 
              on:click={clearFilters}
              class="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Clear all filters
            </button>
          {/if}
        </div>
      {:else}
        <!-- Issues Header -->
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white">
              {filteredIssues.length} issue{filteredIssues.length !== 1 ? 's' : ''}
            </h2>
            <div class="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <div class="w-2 h-2 rounded-full {$websocketStore.connected ? 'bg-green-500' : 'bg-red-500'}"></div>
              <span>{$websocketStore.connected ? 'Live updates' : 'Offline'}</span>
            </div>
          </div>
        </div>
        
        <!-- Issues Table -->
        <div class="overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Issue
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Severity
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Created
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Updated
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {#each filteredIssues as issue (issue.id)}
                  <tr 
                    class="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors duration-150"
                    on:click={() => viewIssue(issue.id)}
                    on:keydown={(e) => e.key === 'Enter' && viewIssue(issue.id)}
                    role="button"
                    tabindex="0"
                  >
                    <td class="px-6 py-4">
                      <div class="flex items-start space-x-3">
                        <div class="flex-shrink-0">
                          {#if issue.file_path}
                            <span class="text-gray-400" title="Has attachment">📎</span>
                          {:else}
                            <span class="text-gray-300">📝</span>
                          {/if}
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                            {issue.title}
                          </p>
                          {#if issue.description}
                            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                              {truncateText(issue.description)}
                            </p>
                          {/if}
                          {#if issue.tags}
                            <div class="mt-2 flex flex-wrap gap-1">
                              {#each issue.tags.split(',').slice(0, 3) as tag}
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                                  {tag.trim()}
                                </span>
                              {/each}
                              {#if issue.tags.split(',').length > 3}
                                <span class="text-xs text-gray-500 dark:text-gray-400">
                                  +{issue.tags.split(',').length - 3} more
                                </span>
                              {/if}
                            </div>
                          {/if}
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(issue.status)}">
                        {issue.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getSeverityColor(issue.severity)}">
                        {issue.severity}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(issue.created_at)}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(issue.updated_at)}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        on:click|stopPropagation={() => viewIssue(issue.id)}
                        class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                      >
                        View
                      </button>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {/if}
    </div>
  </div>