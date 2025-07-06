<!-- frontend/src/routes/issues/create/+page.svelte -->
<script lang="ts">
  import { authStore } from '$lib/stores/auth';
  import { toastStore } from '$lib/stores/toast';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import type { IssueSeverity } from '$lib/types';
  
  let title = '';
  let description = '';
  let severity: IssueSeverity = 'MEDIUM';
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
      
      const issueData = {
        title: title.trim(),
        description: description.trim(),
        severity: severity,
        tags: tags.trim()
      };
      
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/issues/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(issueData)
      });
      
      if (response.ok) {
        const issue = await response.json();
        toastStore.success('Issue Created', 'Your issue has been created successfully');
        goto(`/issues/${issue.id}`);
      } else {
        const errorData = await response.json();
        toastStore.error('Creation Failed', errorData.detail || 'Failed to create issue');
      }
    } catch (error) {
      console.error('Create issue error:', error);
      toastStore.error('Network Error', 'Failed to create issue. Please try again.');
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
      toastStore.error('Invalid File Type', 'Please select an image, PDF, or document.');
      return false;
    }
    
    // Check file size (10MB limit)
    if (selectedFile.size > 10 * 1024 * 1024) {
      toastStore.error('File Too Large', 'Maximum file size is 10MB.');
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
  
  function getSeverityIcon(sev: IssueSeverity): string {
    switch (sev) {
      case 'LOW': return '🟢';
      case 'MEDIUM': return '🟡';
      case 'HIGH': return '🟠';
      case 'CRITICAL': return '🔴';
      default: return '⚪';
    }
  }
  
  function getSeverityColor(sev: IssueSeverity): string {
    switch (sev) {
      case 'LOW': return 'bg-green-50 text-green-800 border-green-200 ring-green-500';
      case 'MEDIUM': return 'bg-yellow-50 text-yellow-800 border-yellow-200 ring-yellow-500';
      case 'HIGH': return 'bg-orange-50 text-orange-800 border-orange-200 ring-orange-500';
      case 'CRITICAL': return 'bg-red-50 text-red-800 border-red-200 ring-red-500';
      default: return 'bg-gray-50 text-gray-800 border-gray-200 ring-gray-500';
    }
  }
</script>

<svelte:head>
  <title>Create New Issue - Issues & Insights Tracker</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="mb-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Create New Issue</h1>
        <p class="mt-2 text-gray-600">
          Report a bug, request a feature, or submit feedback to help improve our system
        </p>
      </div>
      <button
        type="button"
        on:click={handleCancel}
        class="inline-flex items-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
      >
        <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Issues
      </button>
    </div>
  </div>

  <!-- Form Card -->
  <div class="rounded-xl bg-white shadow-sm ring-1 ring-gray-200/50 overflow-hidden">
    <form on:submit|preventDefault={handleSubmit} class="space-y-8 p-8">
      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-semibold text-gray-900 mb-3">
          Issue Title <span class="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          bind:value={title}
          placeholder="Brief description of the issue"
          required
          disabled={loading}
          class="block w-full rounded-lg border-0 py-3 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 transition-all duration-200 text-base"
        />
        <p class="mt-2 text-sm text-gray-600">
          💡 Be specific and concise. This will help others understand the issue quickly.
        </p>
      </div>

      <!-- Severity -->
      <fieldset>
        <legend class="block text-sm font-semibold text-gray-900 mb-4">
          Severity Level
        </legend>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {#each ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as sev}
            <label class="relative cursor-pointer group">
              <input
                type="radio"
                bind:group={severity}
                value={sev}
                disabled={loading}
                class="sr-only"
              />
              <div
                class="flex items-center justify-center rounded-xl border-2 px-4 py-4 text-sm font-semibold transition-all duration-200 group-hover:scale-105
                  {severity === sev
                    ? getSeverityColor(sev) + ' ring-2 ring-offset-2'
                    : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300 hover:bg-gray-50'}"
              >
                <span class="mr-2 text-lg">{getSeverityIcon(sev as IssueSeverity)}</span>
                <span>{sev}</span>
              </div>
            </label>
          {/each}
        </div>
        <p class="mt-3 text-sm text-gray-600">
          🎯 Choose the appropriate severity based on the impact and urgency of the issue.
        </p>
      </fieldset>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-semibold text-gray-900 mb-3">
          Description
        </label>
        <div class="relative">
          <textarea
            id="description"
            bind:value={description}
            rows="6"
            placeholder="Provide detailed information about the issue..."
            disabled={loading}
            class="block w-full rounded-lg border-0 py-3 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 transition-all duration-200 resize-none"
          ></textarea>
          <div class="absolute bottom-3 right-3 text-xs text-gray-400">
            {description.length} characters
          </div>
        </div>
        <div class="mt-3 text-sm text-gray-600">
          <p class="font-medium mb-2">📋 Include these details for better resolution:</p>
          <ul class="list-disc list-inside space-y-1 ml-4">
            <li>Steps to reproduce the issue</li>
            <li>Expected vs actual behavior</li>
            <li>Screenshots or error messages</li>
            <li>Environment details (browser, OS, etc.)</li>
          </ul>
        </div>
      </div>

      <!-- Tags -->
      <div>
        <label for="tags" class="block text-sm font-semibold text-gray-900 mb-3">
          Tags <span class="text-gray-500 font-normal">(Optional)</span>
        </label>
        <input
          type="text"
          id="tags"
          bind:value={tags}
          placeholder="frontend, api, ui, bug, feature (comma-separated)"
          disabled={loading}
          class="block w-full rounded-lg border-0 py-3 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 transition-all duration-200"
        />
        <p class="mt-2 text-sm text-gray-600">
          🏷️ Add relevant tags to help categorize and filter this issue.
        </p>
        {#if tags.trim()}
          <div class="mt-3 flex flex-wrap gap-2">
            {#each tags.split(',') as tag}
              {#if tag.trim()}
                <span class="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800">
                  {tag.trim()}
                </span>
              {/if}
            {/each}
          </div>
        {/if}
      </div>

      <!-- File Upload -->
      <fieldset>
        <legend class="block text-sm font-semibold text-gray-900 mb-4">
          Attachments <span class="text-gray-500 font-normal">(Optional)</span>
        </legend>
        
        <!-- File Drop Zone -->
        <div
          class="relative rounded-xl border-2 border-dashed p-8 text-center transition-all duration-200
            {dragActive
              ? 'border-blue-400 bg-blue-50 scale-105'
              : file
              ? 'border-green-300 bg-green-50'
              : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'}"
          on:drop={handleFileDrop}
          on:dragover={handleDragOver}
          on:dragleave={handleDragLeave}
          role="button"
          tabindex="0"
        >
          {#if file}
            <!-- File Selected -->
            <div class="flex items-center justify-center space-x-4">
              <div class="flex items-center space-x-3">
                <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                  <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="text-left">
                  <p class="text-sm font-medium text-gray-900">{file.name}</p>
                  <p class="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                </div>
              </div>
              <button
                type="button"
                on:click={removeFile}
                disabled={loading}
                aria-label="Remove file"
                class="rounded-full p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-200"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          {:else}
            <!-- Upload Zone -->
            <div>
              <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="space-y-2">
                <label for="file-upload" class="cursor-pointer">
                  <span class="text-base font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200">
                    Upload a file
                  </span>
                  <span class="text-base text-gray-500"> or drag and drop</span>
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
                <p class="text-sm text-gray-500">
                  PNG, JPG, PDF, DOC up to 10MB
                </p>
              </div>
            </div>
          {/if}
        </div>
      </fieldset>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end space-x-4 border-t border-gray-200 pt-8">
        <button
          type="button"
          on:click={handleCancel}
          disabled={loading}
          class="inline-flex items-center rounded-lg border border-gray-300 bg-white px-6 py-3 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-all duration-200"
        >
          Cancel
        </button>
        
        <button
          type="submit"
          disabled={!canSubmit}
          class="inline-flex items-center rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-3 text-sm font-medium text-white shadow-sm hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 disabled:hover:scale-100"
        >
          {#if loading}
            <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Creating Issue...
          {:else}
            <svg class="mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Create Issue
          {/if}
        </button>
      </div>
    </form>
  </div>

  <!-- Tips Card -->
  <div class="mt-8 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 p-6 ring-1 ring-blue-200/50">
    <div class="flex">
      <div class="flex-shrink-0">
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500">
          <svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
      </div>
      <div class="ml-4">
        <h3 class="text-sm font-semibold text-blue-900 mb-3">💡 Tips for creating effective issues</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <ul class="space-y-2">
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Use a clear, descriptive title that summarizes the issue</span>
            </li>
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Include steps to reproduce the problem if it's a bug</span>
            </li>
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Attach screenshots or files that help illustrate the issue</span>
            </li>
          </ul>
          <ul class="space-y-2">
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Choose the appropriate severity level based on impact</span>
            </li>
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Add relevant tags to help with organization and filtering</span>
            </li>
            <li class="flex items-start">
              <span class="mr-2 text-blue-500">•</span>
              <span>Be specific about expected vs actual behavior</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>