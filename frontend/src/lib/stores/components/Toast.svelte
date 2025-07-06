<!-- frontend/src/lib/components/Toast.svelte -->
<script lang="ts">
    import { fly } from 'svelte/transition';
    import { toastStore, type Toast } from '$lib/stores/toast';
    
    $: toasts = $toastStore;
    
    function getToastStyles(type: Toast['type']) {
      switch (type) {
        case 'success':
          return 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900 dark:border-green-700 dark:text-green-300';
        case 'error':
          return 'bg-red-50 border-red-200 text-red-800 dark:bg-red-900 dark:border-red-700 dark:text-red-300';
        case 'warning':
          return 'bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-900 dark:border-yellow-700 dark:text-yellow-300';
        case 'info':
          return 'bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-900 dark:border-blue-700 dark:text-blue-300';
        default:
          return 'bg-gray-50 border-gray-200 text-gray-800 dark:bg-gray-900 dark:border-gray-700 dark:text-gray-300';
      }
    }
    
    function getToastIcon(type: Toast['type']) {
      switch (type) {
        case 'success':
          return '✅';
        case 'error':
          return '❌';
        case 'warning':
          return '⚠️';
        case 'info':
          return 'ℹ️';
        default:
          return '📝';
      }
    }
  </script>
  
  <!-- Toast container -->
  <div class="fixed top-4 right-4 z-50 space-y-2" role="alert" aria-live="polite">
    {#each toasts as toast (toast.id)}
      <div
        transition:fly="{{ x: 300, duration: 300 }}"
        class="flex items-start p-4 border rounded-lg shadow-lg max-w-sm w-full {getToastStyles(toast.type)}"
      >
        <!-- Icon -->
        <div class="flex-shrink-0 mr-3">
          <span class="text-lg">{getToastIcon(toast.type)}</span>
        </div>
        
        <!-- Content -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium">
            {toast.message}
          </p>
        </div>
        
        <!-- Close button -->
        <button
          on:click={() => toastStore.remove(toast.id)}
          class="flex-shrink-0 ml-3 text-lg hover:opacity-70 transition-opacity"
          aria-label="Close notification"
        >
          ×
        </button>
      </div>
    {/each}
  </div>