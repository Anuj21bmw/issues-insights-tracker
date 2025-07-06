<!-- frontend/src/routes/issues/create/+page.svelte -->
<script lang="ts">
    import { authStore } from '$lib/stores/auth';
    import { toastStore } from '$lib/stores/toast';
    import { apiClient } from '$lib/api/client';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    
    let title = '';
    let description = '';
    let severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'MEDIUM';
    let tags = '';
    let file: File | null = null;
    let loading = false;
    let dragActive = false;
    
    $: isAuthenticated = $authStore.isAuthenticated;
    $: user = $authStore.user;
    $: canSubmit = title.trim().length > 0 && !loading;
    
    // File upload handling
    let fileInput: HTMLInputElement;
    
    onMount(() => {
      if (!isAuthenticated) {
        goto('/auth/login');
      }
    });
    
    async function handleSubmit() {
      if (!canSubmit) return;
      
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
        
        const response = await apiClient.createIssue(formData);
        
        if (response.data) {
          toastStore.success('Issue created successfully!');
          goto(`/issues/${response.data.id}`);
        } else {
          toastStore.error(response.error || 'Failed to create issue');
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
        const selectedFile = target.files[0];
        if (validateFile(selectedFile)) {
          file = selectedFile;
        }
      }
    }
    
    function handleFileDrop(event: DragEvent) {
      event.preventDefault();
      dragActive = false;
      
      const files = event.dataTransfer?.files;
      if (files && files[0]) {
        const droppedFile = files[0];
        if (validateFile(droppedFile)) {
          file = droppedFile;
        }
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
    
    function validateFile(selectedFile: File): boolean {
      // Check file type
      const allowedTypes = [
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain', 'text/csv',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];
      
      if (!allowedTypes.includes(selectedFile.type)) {
        toastStore.error('Invalid file type. Please select an image, PDF, or document.');
        return false;
      }
      
      // Check file size (10MB limit)
      if (selectedFile.size > 10 * 1024 * 1024) {
        toastStore.error('File too large. Maximum size is 10MB.');
        return false;
      }
      
      return true;
    }
    
    function formatFileSize(bytes: number): string {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function handleCancel() {
      goto('/issues');
    }
    
    function getSeverityIcon(sev: string): string {
      switch (sev) {
        case 'LOW': return '🟢';
        case 'MEDIUM': return '🟡';
        case 'HIGH': return '🟠';
        case 'CRITICAL': return '🔴';
        default: return '⚪';
      }
    }
    
    function getSeverityColor(sev: string): string {
      switch (sev) {
        case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
        case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
        case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
        default: return 'bg-gray-100 text-gray-800 border-gray-200';
      }
    }
  </script>
  
  <svelte:head>
    <title>Create New Issue - Issue Tracker</title>
  </svelte:head>
  
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Create New Issue</h1>
            <p class="mt-2 text-gray-600">
              Report a bug, request a feature, or submit feedback
            </p>
          </div>
          <button
            type="button"
            on:click={handleCancel}
            class="rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            ← Back to Issues
          </button>
        </div>
      </div>
  
      <!-- Form Card -->
      <div class="rounded-lg bg-white shadow-sm ring-1 ring-gray-200">
        <form on:submit|preventDefault={handleSubmit} class="space-y-6 p-6">
          <!-- Title -->
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
              Issue Title <span class="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="title"
              bind:value={title}
              placeholder="Brief description of the issue"
              required
              disabled={loading}
              class="block w-full rounded-lg border-gray-300 px-3 py-2 text-sm placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
            />
            <p class="mt-1 text-xs text-gray-500">
              Be specific and concise. This will help others understand the issue quickly.
            </p>
          </div>
  
          <!-- Severity -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">
              Severity Level
            </label>
            <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
              {#each ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as sev}
                <label class="relative cursor-pointer">
                  <input
                    type="radio"
                    bind:group={severity}
                    value={sev}
                    disabled={loading}
                    class="sr-only"
                  />
                  <div
                    class="flex items-center justify-center rounded-lg border-2 px-3 py-3 text-sm font-medium transition-all
                      {severity === sev
                        ? getSeverityColor(sev) + ' ring-2 ring-blue-500'
                        : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'}"
                  >
                    <span class="mr-2">{getSeverityIcon(sev)}</span>
                    {sev}
                  </div>
                </label>
              {/each}
            </div>
          </div>
  
          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              bind:value={description}
              rows="6"
              placeholder="Provide detailed information about the issue, including steps to reproduce, expected behavior, and actual behavior..."
              disabled={loading}
              class="block w-full rounded-lg border-gray-300 px-3 py-2 text-sm placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
            ></textarea>
            <p class="mt-1 text-xs text-gray-500">
              Include as much detail as possible. Screenshots, error messages, and reproduction steps are helpful.
            </p>
          </div>
  
          <!-- Tags -->
          <div>
            <label for="tags" class="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <input
              type="text"
              id="tags"
              bind:value={tags}
              placeholder="frontend, api, ui, bug, feature (comma-separated)"
              disabled={loading}
              class="block w-full rounded-lg border-gray-300 px-3 py-2 text-sm placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
            />
            <p class="mt-1 text-xs text-gray-500">
              Add relevant tags to help categorize and filter this issue (optional).
            </p>
          </div>
  
          <!-- File Upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">
              Attachments
            </label>
            
            <!-- File Drop Zone -->
            <div
              class="relative rounded-lg border-2 border-dashed p-6 transition-colors
                {dragActive
                  ? 'border-blue-400 bg-blue-50'
                  : file
                  ? 'border-green-300 bg-green-50'
                  : 'border-gray-300 hover:border-gray-400'}"
              on:drop={handleFileDrop}
              on:dragover={handleDragOver}
              on:dragleave={handleDragLeave}
              role="button"
              tabindex="0"
            >
              {#if file}
                <!-- File Selected -->
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100">
                      📎
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{file.name}</p>
                      <p class="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    on:click={removeFile}
                    disabled={loading}
                    class="rounded-full p-1 text-gray-400 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-red-500"
                  >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              {:else}
                <!-- Upload Zone -->
                <div class="text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="mt-4">
                    <label for="file-upload" class="cursor-pointer">
                      <span class="text-sm font-medium text-blue-600 hover:text-blue-500">
                        Upload a file
                      </span>
                      <span class="text-sm text-gray-500"> or drag and drop</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        bind:this={fileInput}
                        on:change={handleFileSelect}
                        disabled={loading}
                        class="sr-only"
                      />
                    </label>
                  </div>
                  <p class="text-xs text-gray-500 mt-2">
                    PNG, JPG, PDF up to 10MB
                  </p>
                </div>
              {/if}
            </div>
          </div>
  
          <!-- Action Buttons -->
          <div class="flex items-center justify-end space-x-3 border-t border-gray-200 pt-6">
            <button
              type="button"
              on:click={handleCancel}
              disabled={loading}
              class="rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Cancel
            </button>
            
            <button
              type="submit"
              disabled={!canSubmit}
              class="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {#if loading}
                <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              {:else}
                Create Issue
              {/if}
            </button>
          </div>
        </form>
      </div>
  
      <!-- Tips Card -->
      <div class="mt-8 rounded-lg bg-blue-50 p-6">
        <h3 class="text-sm font-medium text-blue-900 mb-3">💡 Tips for creating effective issues</h3>
        <ul class="space-y-2 text-sm text-blue-800">
          <li class="flex items-start">
            <span class="mr-2">•</span>
            <span>Use a clear, descriptive title that summarizes the issue</span>
          </li>
          <li class="flex items-start">
            <span class="mr-2">•</span>
            <span>Include steps to reproduce the problem if it's a bug</span>
          </li>
          <li class="flex items-start">
            <span class="mr-2">•</span>
            <span>Attach screenshots or files that help illustrate the issue</span>
          </li>
          <li class="flex items-start">
            <span class="mr-2">•</span>
            <span>Choose the appropriate severity level based on impact</span>
          </li>
          <li class="flex items-start">
            <span class="mr-2">•</span>
            <span>Add relevant tags to help with organization and filtering</span>
          </li>
        </ul>
      </div>
    </div>
  </div>