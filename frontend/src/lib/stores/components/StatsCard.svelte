<!-- frontend/src/lib/components/StatsCard.svelte -->
<script lang="ts">
    export let title: string;
    export let value: number | string;
    export let icon: string;
    export let trend: 'positive' | 'negative' | 'neutral' | 'warning' | 'info' = 'neutral';
    export let subtitle: string = '';
    export let href: string = '';
    
    function getTrendColor(trend: string): string {
      switch (trend) {
        case 'positive':
          return 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900';
        case 'negative':
          return 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900';
        case 'warning':
          return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900';
        case 'info':
          return 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900';
        default:
          return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-900';
      }
    }
    
    $: trendColors = getTrendColor(trend);
    $: isClickable = !!href;
  </script>
  
  <svelte:element 
    this={isClickable ? 'a' : 'div'}
    {href}
    class="block bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6
           {isClickable ? 'hover:shadow-md hover:border-gray-300 dark:hover:border-gray-600 transition-all duration-200 cursor-pointer' : ''}"
  >
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
          {title}
        </p>
        <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </p>
        {#if subtitle}
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {subtitle}
          </p>
        {/if}
      </div>
      
      <div class="flex-shrink-0">
        <div class="w-12 h-12 rounded-lg flex items-center justify-center {trendColors}">
          <span class="text-2xl">{icon}</span>
        </div>
      </div>
    </div>
    
    {#if isClickable}
      <div class="mt-4 flex items-center text-sm text-blue-600 dark:text-blue-400">
        <span>View details</span>
        <svg class="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </div>
    {/if}
  </svelte:element>