<!-- frontend/src/routes/issues/[id]/+page.svelte -->
<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { authStore } from '$lib/stores/auth';
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
    
    let issue: Issue | null = null;
    let loading = true;
    let error = '';
    let editing = false;
    let saving = false;
    
    // Edit form data
    let editTitle = '';
    let editDescription = '';
    let editStatus: Issue['status'] = 'OPEN';
    let editSeverity: Issue['severity'] = 'MEDIUM';
    let editTags = '';
    
    $: issueId = $page.params.id;
    $: token = $authStore.token;
    $: user = $authStore.user;
    $: canEdit = user && (user.role === 'ADMIN' || user.role === 'MAINTAINER' || 
      (user.role === 'REPORTER' && issue?.created_by === user.id));
    $: canDelete = user?.role === 'ADMIN';
    
    onMount(() => {
      if (!$authStore.isAuthenticated) {
        goto('/auth/login');
        return;
      }
      
      loadIssue();
      
      // Listen for real-time updates
      const handleIssueUpdated = (event: CustomEvent) => {
        const updatedIssue = event.detail;
        if (updatedIssue.id === issueId) {
          issue = updatedIssue;
          toastStore.info('Issue updated by another user');
        }
      };
      
      const handleIssueDeleted = (event: CustomEvent) => {
        const { id } = event.detail;
        if (id === issueId) {
          toastStore.warning('This issue was deleted');
          goto('/issues');
        }
      };
      
      window.addEventListener('issue-updated', handleIssueUpdated as EventListener);
      window.addEventListener('issue-deleted', handleIssueDeleted as EventListener);
      
      return () => {
        window.removeEventListener('issue-updated', handleIssueUpdated as EventListener);
        window.removeEventListener('issue-deleted', handleIssueDeleted as EventListener);
      };
    });
    
    async function loadIssue() {
      if (!token || !issueId) return;
      
      try {
        loading = true;
        error = '';
        
        const response = await fetch(`http://localhost:8000/api/issues/${issueId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          issue = await response.json();
          // Initialize edit form with current values
          if (issue) {
            editTitle = issue.title;
            editDescription = issue.description || '';
            editStatus = issue.status;
            editSeverity = issue.severity;
            editTags = issue.tags || '';
          }
        } else if (response.status === 404) {
          error = 'Issue not found';
        } else if (response.status === 403) {
          error = 'Access denied';
        } else {
          error = 'Failed to load issue';
        }
      } catch (err) {
        error = 'Network error loading issue';
        console.error('Issue detail error:', err);
      } finally {
        loading = false;
      }
    }
    
    async function handleSave() {
      if (!token || !issue || saving) return;
      
      try {
        saving = true;
        
        const updateData: any = {};
        
        // Only include changed fields
        if (editTitle !== issue.title) updateData.title = editTitle;
        if (editDescription !== (issue.description || '')) updateData.description = editDescription;
        if (editStatus !== issue.status) updateData.status = editStatus;
        if (editSeverity !== issue.severity) updateData.severity = editSeverity;
        if (editTags !== (issue.tags || '')) updateData.tags = editTags;
        
        if (Object.keys(updateData).length === 0) {
          editing = false;
          return;
        }
        
        const response = await fetch(`http://localhost:8000/api/issues/${issue.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updateData)
        });
        
        if (response.ok) {
          const updatedIssue = await response.json();
          issue = updatedIssue;
          editing = false;
          toastStore.success('Issue updated successfully');
        } else {
          const error = await response.json();
          toastStore.error(error.detail || 'Failed to update issue');
        }
      } catch (error) {
        console.error('Update issue error:', error);
        toastStore.error('Network error. Please try again.');
      } finally {
        saving = false;
      }
    }
    
    async function handleDelete() {
      if (!token || !issue || !canDelete) return;
      
      if (!confirm('Are you sure you want to delete this issue? This action cannot be undone.')) {
        return;
      }
      
      try {
        const response = await fetch(`http://localhost:8000/api/issues/${issue.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          toastStore.success('Issue deleted successfully');
          goto('/issues');
        } else {
          const error = await response.json();
          toastStore.error(error.detail || 'Failed to delete issue');
        }
      } catch (error) {
        console.error('Delete issue error:', error);
        toastStore.error('Network error. Please try again.');
      }
    }
    
    function startEditing() {
      if (!canEdit) return;
      editing = true;
    }
    
    function cancelEditing() {
      if (!issue) return;
      
      // Reset form to original values
      editTitle = issue.title;
      editDescription = issue.description || '';
      editStatus = issue.status;
      editSeverity = issue.severity;
      editTags = issue.tags || '';
      editing = false;
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
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
    
    function getFileIcon(fileName: string): string {
      const ext = fileName.split('.').pop()?.toLowerCase();
      switch (ext) {
        case 'pdf': return '📄';
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif': return '🖼️';
        case 'doc':
        case 'docx': return '📝';
        case 'txt': return '📋';
        case 'csv': return '📊';
        default: return '📎';
      }
    }
    
    function downloadFile() {
      if (issue?.file_path) {
        window.open(`http://localhost:8000/uploads/${issue.file_path.split('/').pop()}`, '_blank');
      }
    }
  </script>
  
  <svelte:head>
    <title>{issue ? issue.title : 'Issue'} - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="max-w-4xl mx-auto space-y-6">
    {#if loading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading issue...</span>
      </div>
    {:else if error}
      <div class="text-center py-12">
        <div class="text-red-600 dark:text-red-400 mb-4">
          <span class="text-6xl">❌</span>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Issue Not Found</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
        <button 
          on:click={() => goto('/issues')}
          class="text-blue-600 dark:text-blue-400 hover:underline"
        >
          ← Back to Issues
        </button>
      </div>
    {:else if issue}
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div class="flex-1">
          <nav class="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400 mb-4">
            <a href="/issues" class="hover:text-gray-700 dark:hover:text-gray-300">Issues</a>
            <span>›</span>
            <span class="text-gray-900 dark:text-white">{issue.title}</span>
          </nav>
          
          {#if editing}
            <input
              bind:value={editTitle}
              class="text-3xl font-bold bg-transparent border-b-2 border-blue-500 text-gray-900 dark:text-white focus:outline-none w-full"
              disabled={saving}
            />
          {:else}
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{issue.title}</h1>
          {/if}
          
          <div class="flex flex-wrap items-center gap-4 mt-4">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium {getStatusColor(editing ? editStatus : issue.status)}">
              {#if editing}
                <select bind:value={editStatus} disabled={saving} class="bg-transparent border-none outline-none">
                  <option value="OPEN">OPEN</option>
                  <option value="TRIAGED">TRIAGED</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="DONE">DONE</option>
                </select>
              {:else}
                {issue.status.replace('_', ' ')}
              {/if}
            </span>
            
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium {getSeverityColor(editing ? editSeverity : issue.severity)}">
              {#if editing}
                <select bind:value={editSeverity} disabled={saving} class="bg-transparent border-none outline-none">
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                  <option value="CRITICAL">CRITICAL</option>
                </select>
              {:else}
                {issue.severity}
              {/if}
            </span>
            
            <span class="text-sm text-gray-500 dark:text-gray-400">
              ID: {issue.id.split('-')[0]}...
            </span>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center space-x-2">
          {#if editing}
            <button
              on:click={cancelEditing}
              disabled={saving}
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              on:click={handleSave}
              disabled={saving}
              class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
          {:else}
            {#if canEdit}
              <button
                on:click={startEditing}
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                Edit
              </button>
            {/if}
            
            {#if canDelete}
              <button
                on:click={handleDelete}
                class="px-4 py-2 border border-red-300 dark:border-red-600 rounded-md text-sm font-medium text-red-700 dark:text-red-300 bg-white dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                Delete
              </button>
            {/if}
          {/if}
        </div>
      </div>
      
      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Description -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Description</h2>
            
            {#if editing}
              <textarea
                bind:value={editDescription}
                placeholder="Issue description..."
                rows="8"
                disabled={saving}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 resize-vertical"
              ></textarea>
            {:else if issue.description}
              <div class="prose dark:prose-invert max-w-none">
                <pre class="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 font-sans">{issue.description}</pre>
              </div>
            {:else}
              <p class="text-gray-500 dark:text-gray-400 italic">No description provided</p>
            {/if}
          </div>
          
          <!-- Attachment -->
          {#if issue.file_path}
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Attachment</h2>
              
              <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="flex items-center space-x-3">
                  <span class="text-2xl">{getFileIcon(issue.file_path)}</span>
                  <div>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">
                      {issue.file_path.split('/').pop()}
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Attachment</p>
                  </div>
                </div>
                <button
                  on:click={downloadFile}
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                >
                  Download
                </button>
              </div>
            </div>
          {/if}
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Details -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Details</h2>
            
            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Created</dt>
                <dd class="text-sm text-gray-900 dark:text-white">{formatDate(issue.created_at)}</dd>
              </div>
              
              <div>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</dt>
                <dd class="text-sm text-gray-900 dark:text-white">{formatDate(issue.updated_at)}</dd>
              </div>
              
              <div>
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Reporter</dt>
                <dd class="text-sm text-gray-900 dark:text-white">{issue.created_by}</dd>
              </div>
              
              {#if issue.assigned_to}
                <div>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Assignee</dt>
                  <dd class="text-sm text-gray-900 dark:text-white">{issue.assigned_to}</dd>
                </div>
              {/if}
            </dl>
          </div>
          
          <!-- Tags -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Tags</h2>
            
            {#if editing}
              <input
                bind:value={editTags}
                placeholder="tag1, tag2, tag3"
                disabled={saving}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
              />
            {:else if issue.tags}
              <div class="flex flex-wrap gap-2">
                {#each issue.tags.split(',') as tag}
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                    {tag.trim()}
                  </span>
                {/each}
              </div>
            {:else}
              <p class="text-gray-500 dark:text-gray-400 text-sm">No tags</p>
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </div>