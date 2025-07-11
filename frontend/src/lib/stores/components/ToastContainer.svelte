<!-- src/lib/stores/components/ToastContainer.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { flip } from 'svelte/animate';
  import { toasts } from '$lib/stores/toast';
  import type { Toast } from '$lib/types';

  function getIcon(type: Toast['type']) {
    switch (type) {
      case 'success':
        return `<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>`;
      case 'error':
        return `<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>`;
      case 'warning':
        return `<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>`;
      case 'info':
        return `<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>`;
      default:
        return '';
    }
  }

  function getToastClasses(type: Toast['type']) {
    const baseClasses = "relative rounded-xl p-4 shadow-lg ring-1 backdrop-blur-sm transition-all duration-300";
    switch (type) {
      case 'success':
        return `${baseClasses} bg-green-50/90 ring-green-200/50 text-green-800`;
      case 'error':
        return `${baseClasses} bg-red-50/90 ring-red-200/50 text-red-800`;
      case 'warning':
        return `${baseClasses} bg-amber-50/90 ring-amber-200/50 text-amber-800`;
      case 'info':
        return `${baseClasses} bg-blue-50/90 ring-blue-200/50 text-blue-800`;
      default:
        return `${baseClasses} bg-gray-50/90 ring-gray-200/50 text-gray-800`;
    }
  }

  function getIconColor(type: Toast['type']) {
    switch (type) {
      case 'success':
        return 'text-green-500';
      case 'error':
        return 'text-red-500';
      case 'warning':
        return 'text-amber-500';
      case 'info':
        return 'text-blue-500';
      default:
        return 'text-gray-500';
    }
  }

  function getProgressBarColor(type: Toast['type']) {
    switch (type) {
      case 'success':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      case 'warning':
        return 'bg-amber-500';
      case 'info':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  }
</script>

<div class="fixed top-4 right-4 z-50 space-y-3 max-w-sm w-full pointer-events-none">
  {#each $toasts as toast (toast.id)}
    <div
      animate:flip={{ duration: 300 }}
      in:fly={{ x: 300, duration: 300, delay: 0 }}
      out:fade={{ duration: 200 }}
      class="{getToastClasses(toast.type)} pointer-events-auto"
    >
      <!-- Progress bar for timed toasts -->
      {#if toast.duration && toast.duration > 0}
        <div class="absolute bottom-0 left-0 right-0 h-1 bg-black/5 rounded-b-xl overflow-hidden">
          <div 
            class="{getProgressBarColor(toast.type)} h-full rounded-b-xl transition-all duration-100 ease-linear"
            style="animation: shrink {toast.duration}ms linear forwards;"
          ></div>
        </div>
      {/if}

      <div class="flex items-start">
        <!-- Icon -->
        <div class="flex-shrink-0">
          <div class="{getIconColor(toast.type)}">
            {@html getIcon(toast.type)}
          </div>
        </div>
        
        <!-- Content -->
        <div class="ml-3 flex-1 min-w-0">
          <h3 class="text-sm font-semibold leading-5">
            {toast.title}
          </h3>
          {#if toast.message}
            <p class="mt-1 text-sm opacity-90 leading-relaxed">
              {toast.message}
            </p>
          {/if}
        </div>
        
        <!-- Close button -->
        <div class="ml-4 flex-shrink-0">
          <button
            on:click={() => toasts.remove(toast.id)}
            class="inline-flex rounded-lg p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-200 hover:bg-black/5 focus:bg-black/5"
            aria-label="Close notification"
          >
            <svg class="h-4 w-4 opacity-60 hover:opacity-100" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  {/each}
</div>

<style>
  @keyframes shrink {
    from {
      width: 100%;
    }
    to {
      width: 0%;
    }
  }
</style>