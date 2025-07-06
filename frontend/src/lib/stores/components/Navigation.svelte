<!-- frontend/src/lib/components/Navigation.svelte -->
<script lang="ts">
    import { authStore } from '$lib/stores/auth';
    import { page } from '$app/stores';
    import { websocketStore } from '$lib/stores/websocket';
    
    $: user = $authStore.user;
    $: currentPath = $page.url.pathname;
    $: isConnected = $websocketStore.connected;
    
    function handleLogout() {
      authStore.logout();
    }
    
    // Navigation items based on user role
    $: navItems = [
      { href: '/dashboard', label: 'Dashboard', icon: '📊', roles: ['ADMIN', 'MAINTAINER', 'REPORTER'] },
      { href: '/issues', label: 'Issues', icon: '🐛', roles: ['ADMIN', 'MAINTAINER', 'REPORTER'] },
      { href: '/issues/create', label: 'Create Issue', icon: '➕', roles: ['ADMIN', 'MAINTAINER', 'REPORTER'] },
      { href: '/users', label: 'Users', icon: '👥', roles: ['ADMIN'] },
      { href: '/stats', label: 'Statistics', icon: '📈', roles: ['ADMIN', 'MAINTAINER'] }
    ].filter(item => user && item.roles.includes(user.role));
    
    function isActive(href: string): boolean {
      return currentPath === href || (href !== '/dashboard' && currentPath.startsWith(href));
    }
  </script>
  
  <nav class="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and title -->
        <div class="flex items-center space-x-4">
          <a href="/dashboard" class="flex items-center space-x-2">
            <span class="text-2xl">🔍</span>
            <span class="text-xl font-bold text-gray-900 dark:text-white">
              Issues & Insights
            </span>
          </a>
          
          <!-- Connection status -->
          <div class="flex items-center space-x-1">
            <div class="w-2 h-2 rounded-full {isConnected ? 'bg-green-500' : 'bg-red-500'}"></div>
            <span class="text-xs text-gray-500 dark:text-gray-400">
              {isConnected ? 'Live' : 'Offline'}
            </span>
          </div>
        </div>
        
        <!-- Main navigation -->
        <div class="hidden md:flex items-center space-x-1">
          {#each navItems as item}
            <a
              href={item.href}
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200
                     {isActive(item.href) 
                       ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300' 
                       : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
            >
              <span class="mr-1">{item.icon}</span>
              {item.label}
            </a>
          {/each}
        </div>
        
        <!-- User menu -->
        <div class="flex items-center space-x-4">
          <!-- User info -->
          <div class="hidden sm:flex items-center space-x-2">
            <div class="text-right">
              <div class="text-sm font-medium text-gray-900 dark:text-white">
                {user?.name || user?.email}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {user?.role}
              </div>
            </div>
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <span class="text-white text-sm font-medium">
                {user?.name?.charAt(0) || user?.email?.charAt(0) || '?'}
              </span>
            </div>
          </div>
          
          <!-- Logout button -->
          <button
            on:click={handleLogout}
            class="flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium
                   text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700
                   transition-colors duration-200"
          >
            <span>🚪</span>
            <span class="hidden sm:inline">Logout</span>
          </button>
        </div>
        
        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button
            class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
            aria-label="Open mobile menu"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile navigation -->
      <div class="md:hidden border-t border-gray-200 dark:border-gray-700 py-2">
        {#each navItems as item}
          <a
            href={item.href}
            class="block px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200
                   {isActive(item.href) 
                     ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300' 
                     : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
          >
            <span class="mr-2">{item.icon}</span>
            {item.label}
          </a>
        {/each}
      </div>
    </div>
  </nav>