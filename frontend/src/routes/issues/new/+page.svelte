<!-- src/routes/issues/new/+page.svelte -->
<script lang="ts">
    import { goto } from '$app/navigation';
    import { toasts } from '$lib/stores/toast';
    import type { Issue } from '$lib/types';
    
    let title = '';
    let description = '';
    let isLoading = false;
    let error = '';
  
    async function handleSubmit(event: Event): Promise<void> {
      event.preventDefault();
      isLoading = true;
      error = '';
  
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:8000/api/issues/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            title,
            description
          })
        });
  
        if (response.ok) {
          const issue: Issue = await response.json();
          toasts.success('Issue Created', 'Your issue has been created successfully');
          goto(`/issues/${issue.id}`);
        } else {
          const data = await response.json();
          error = data.detail || 'Failed to create issue';
          toasts.error('Creation Failed', error);
        }
      } catch (err) {
        error = 'Network error. Please try again.';
        toasts.error('Network Error', error);
      } finally {
        isLoading = false;
      }
    }
  </script>
  
  <svelte:head>
    <title>Create New Issue - Issue Tracker</title>
  </svelte:head>
  
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-8">
      <nav class="flex" aria-label="Breadcrumb">
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
              <span class="ml-4 text-sm font-medium text-gray-500">New Issue</span>
            </div>
          </li>
        </ol>
      </nav>
      
      <h1 class="mt-4 text-3xl font-bold text-gray-900">Create New Issue</h1>
      <p class="mt-2 text-gray-600">Report a bug, request a feature, or ask a question</p>
    </div>
  
    <div class="bg-white shadow-sm rounded-lg border border-gray-200">
      <form on:submit={handleSubmit} class="space-y-6 p-6">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
            Issue Title *
          </label>
          <input
            id="title"
            name="title"
            type="text"
            required
            bind:value={title}
            placeholder="Brief description of the issue"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
          <p class="mt-1 text-xs text-gray-500">
            Choose a clear, descriptive title that summarizes the issue
          </p>
        </div>
  
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            rows="6"
            bind:value={description}
            placeholder="Provide detailed information about the issue, including:&#10;- Steps to reproduce (for bugs)&#10;- Expected behavior&#10;- Actual behavior&#10;- Screenshots or error messages (if applicable)&#10;- Additional context"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          ></textarea>
          <p class="mt-1 text-xs text-gray-500">
            The more details you provide, the easier it will be to address the issue
          </p>
        </div>
  
        {#if error}
          <div class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
            {error}
          </div>
        {/if}
  
        <div class="flex items-center justify-between pt-4 border-t border-gray-200">
          <a href="/issues" 
             class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors">
            Cancel
          </a>
          <button
            type="submit"
            disabled={isLoading || !title.trim()}
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {#if isLoading}
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            {/if}
            {isLoading ? 'Creating...' : 'Create Issue'}
          </button>
        </div>
      </form>
    </div>
  
    <!-- Tips Section -->
    <div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-blue-800">Tips for writing good issues</h3>
          <div class="mt-2 text-sm text-blue-700">
            <ul class="list-disc list-inside space-y-1">
              <li>Use a clear and specific title</li>
              <li>Include steps to reproduce the problem</li>
              <li>Mention your environment (browser, OS, etc.)</li>
              <li>Add screenshots or error messages when helpful</li>
              <li>Check if the issue already exists before creating</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>