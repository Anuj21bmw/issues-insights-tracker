<!-- frontend/src/routes/issues/create/+page.svelte -->
<script lang="ts">
    import { authStore } from '$lib/stores/auth';
    import { toastStore } from '$lib/stores/toast';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    
    let title = '';
    let description = '';
    let severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'MEDIUM';
    let tags = '';
    let file: File | null = null;
    let loading = false;
    let dragActive = false;
    
    $: token = $authStore.token;
    $: user = $authStore.user;
    $: canSubmit = title.trim().length > 0 && !loading;
    
    // File upload handling
    let fileInput: HTMLInputElement;
    
    onMount(() => {
      if (!$authStore.isAuthenticated) {
        goto('/auth/login');
      }
    });
    
    async function handleSubmit() {
      if (!canSubmit || !token) return;
      
      try {
        loading = true;
        
        const formData = new FormData();
        formData.append('title', title.trim());
        formData.append('description', description.trim());
        formData.append('severity', severity);
        formData.append('tags', tags.trim());
        
        if (file) {
          formData.append('file', file);
        }
        
        const response = await fetch('http://localhost:8000/api/issues/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });
        
        if (response.ok) {
          const newIssue = await response.json();
          toastStore.success('Issue created successfully!');
          goto(`/issues/${newIssue.id}`);
        } else {
          const error = await response.json();
          toastStore.error(error.detail || 'Failed to create issue');
        }
      } catch (error) {
        console.error('Create issue error:', error);
        toastStore.error('Network error. Please try again.');
      } finally {
        loading = false;
      }
    }
    
    function handleFileSelect(event: Event) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        file = target.files[0];
      }
    }
    
    function handleFileDrop(event: DragEvent) {
      event.preventDefault();
      dragActive = false;
      
      const files = event.dataTransfer?.files;
      if (files && files[0]) {
        file = files[0];
      }
    }
    
    function handleDragOver(event: DragEvent) {
      event.preventDefault();
      dragActive = true;
    }
    
    function handleDragLeave(event: DragEvent) {
      event.preventDefault();
      dragActive = false;
    }
    
    function removeFile() {
      file = null;
      if (fileInput) {
        fileInput.value = '';
      }
    }
    
    function formatFileSize(bytes: number): string {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function isValidFileType(file: File): boolean {
      const allowedTypes = [
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain', 'text/csv',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];
      return allowedTypes.includes(file.type);
    }
    
    function handleCancel() {
      goto('/issues');
    }
    
    $: if (file && !isValidFileType(file)) {
      toastStore.error('Invalid file type. Please select an image, PDF, or document.');
      removeFile();
    }
    
    $: if (file && file.size > 10 * 1024 * 1024) { // 10MB limit
      toastStore.error('File too large. Maximum size is 10MB.');
      removeFile();
    }
  </script>
  
  <svelte:head>
    <title>Create Issue - Issues & Insights Tracker</title>
  </svelte:head>
  
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Create New Issue</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-1">
        Report a new issue or bug for tracking
      </p>
    </div>
    
    <!-- Form -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <form on:submit|preventDefault={handleSubmit} class="p-8 space-y-6">
        <!-- Title -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Title <span class="text-red-500">*</span>
          </label>
          <input
            id="title"
            type="text"
            bind:value={title}
            placeholder="Brief description of the issue"
            required
            disabled={loading}
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>
        
        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description
          </label>
          <textarea
            id="description"
            bind:value={description}
            placeholder="Detailed description of the issue. You can use Markdown formatting."
            rows="6"
            disabled={loading}
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed resize-vertical"
          ></textarea>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Tip: Use Markdown for formatting (bold, italic, lists, etc.)
          </p>
        </div>
        
        <!-- Severity and Tags Row -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Severity -->
          <div>
            <label for="severity" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Severity
            </label>
            <select
              id="severity"
              bind:value={severity}
              disabled={loading}
              class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <option value="LOW">🟢 Low</option>
              <option value="MEDIUM">🟡 Medium</option>
              <option value="HIGH">🟠 High</option>
              <option value="CRITICAL">🔴 Critical</option>
            </select>
          </div>
          
          <!-- Tags -->
          <div>
            <label for="tags" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Tags
            </label>
            <input
              id="tags"
              type="text"
              bind:value={tags}
              placeholder="bug, ui, mobile (comma-separated)"
              disabled={loading}
              class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Separate multiple tags with commas
            </p>
          </div>
        </div>
        
        <!-- File Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Attachment (Optional)
          </label>
          
          {#if file}
            <!-- Selected File Display -->
            <div class="border border-gray-200 dark:border-gray-600 rounded-lg p-4 bg-gray-50 dark:bg-gray-700">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <span class="text-2xl">📎</span>
                  <div>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{file.name}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <button
                  type="button"
                  on:click={removeFile}
                  disabled={loading}
                  class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 disabled:opacity-50"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>
          {:else}
            <!-- File Drop Zone -->
            <div
              class="border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 {dragActive ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600'}"
              on:drop={handleFileDrop}
              on:dragover={handleDragOver}
              on:dragleave={handleDragLeave}
            >
              <div class="space-y-4">
                <div class="text-4xl">📎</div>
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    Drop a file here, or 
                    <button
                      type="button"
                      on:click={() => fileInput?.click()}
                      disabled={loading}
                      class="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 disabled:opacity-50"
                    >
                      browse
                    </button>
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Images, PDFs, and documents up to 10MB
                  </p>
                </div>
              </div>
            </div>
            
            <input
              bind:this={fileInput}
              type="file"
              on:change={handleFileSelect}
              accept=".jpg,.jpeg,.png,.gif,.pdf,.txt,.csv,.doc,.docx"
              disabled={loading}
              class="hidden"
            />
          {/if}
        </div>
        
        <!-- Actions -->
        <div class="flex flex-col sm:flex-row sm:justify-end space-y-3 sm:space-y-0 sm:space-x-3 pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            type="button"
            on:click={handleCancel}
            disabled={loading}
            class="w-full sm:w-auto px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            Cancel
          </button>
          
          <button
            type="submit"
            disabled={!canSubmit}
            class="w-full sm:w-auto px-6 py-3 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {#if loading}
              <span class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </span>
            {:else}
              Create Issue
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>