<!-- src/lib/components/Navigation.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
  import { authStore } from '$lib/stores/auth';
  import { toasts } from '$lib/stores/toast';
  import { goto } from '$app/navigation';
  
  $: isAuthenticated = $authStore.isAuthenticated;
  $: user = $authStore.user;
  $: currentPath = $page.url.pathname;
  
  let mobileMenuOpen = false;
  let userMenuOpen = false;
  
  function handleLogout() {
    authStore.logout();
    toasts.success('Logged Out', 'You have been logged out successfully');
    goto('/');
    userMenuOpen = false;
  }
  
  function closeMobileMenu() {
    mobileMenuOpen = false;
  }
  
  function closeUserMenu() {
    userMenuOpen = false;
  }
  
  function isCurrentPath(path: string): boolean {
    return currentPath === path || currentPath.startsWith(path + '/');
  }
  
  // Close menus when clicking outside
  function handleClickOutside(event: MouseEvent) {
    const target = event.target as Element;
    if (!target.closest('.user-menu') && !target.closest('.user-menu-button')) {
      userMenuOpen = false;
    }
    if (!target.closest('.mobile-menu') && !target.closest('.mobile-menu-button')) {
      mobileMenuOpen = false;
    }
  }
</script>

<svelte:window on:click={handleClickOutside} />

<nav class="bg-white shadow-sm border-b border-gray-200">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex h-16 justify-between">
      <!-- Logo and main nav -->
      <div class="flex">
        <div class="flex flex-shrink-0 items-center">
          <a href="/" class="text-xl font-bold text-gray-900">
            🐛 Issue Tracker
          </a>
        </div>
        
        {#if isAuthenticated}
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <a
              href="/dashboard"
              class="inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium transition-colors
                {isCurrentPath('/dashboard') 
                  ? 'border-blue-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}"
            >
              Dashboard
            </a>
            <a
              href="/issues"
              class="inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium transition-colors
                {isCurrentPath('/issues') 
                  ? 'border-blue-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}"
            >
              Issues
            </a>
            <a
              href="/issues/create"
              class="inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium transition-colors
                {isCurrentPath('/issues/create') 
                  ? 'border-blue-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}"
            >
              Create Issue
            </a>
            {#if user?.role === 'ADMIN'}
              <a
                href="/admin"
                class="inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium transition-colors
                  {isCurrentPath('/admin') 
                    ? 'border-blue-500 text-gray-900' 
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}"
              >
                Admin
              </a>
            {/if}
          </div>
        {/if}
      </div>

      <!-- Right side -->
      <div class="hidden sm:ml-6 sm:flex sm:items-center">
        {#if isAuthenticated && user}
          <!-- User menu -->
          <div class="relative ml-3 user-menu">
            <button
              type="button"
              class="user-menu-button flex rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              on:click={() => userMenuOpen = !userMenuOpen}
            >
              <span class="sr-only">Open user menu</span>
              <div class="flex items-center space-x-3 rounded-full bg-gray-100 px-3 py-2">
                <div class="h-6 w-6 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-medium">
                  {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                </div>
                <span class="text-sm font-medium text-gray-700">{user.name || user.email}</span>
                <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </button>

            {#if userMenuOpen}
              <div class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5">
                <div class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm text-gray-500">Signed in as</p>
                  <p class="text-sm font-medium text-gray-900">{user.name || user.email}</p>
                  <p class="text-xs text-gray-500 capitalize">{user.role.toLowerCase()} Role</p>
                </div>
                <a
                  href="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  on:click={closeUserMenu}
                >
                  Your Profile
                </a>
                <a
                  href="/settings"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  on:click={closeUserMenu}
                >
                  Settings
                </a>
                <button
                  type="button"
                  class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
                  on:click={handleLogout}
                >
                  Sign out
                </button>
              </div>
            {/if}
          </div>
        {:else}
          <!-- Login/Register buttons -->
          <div class="flex items-center space-x-4">
            <a
              href="/auth/login"
              class="text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              Sign in
            </a>
            <a
              href="/auth/register"
              class="rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Sign up
            </a>
          </div>
        {/if}
      </div>

      <!-- Mobile menu button -->
      <div class="-mr-2 flex items-center sm:hidden">
        <button
          type="button"
          class="mobile-menu-button inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          on:click={() => mobileMenuOpen = !mobileMenuOpen}
        >
          <span class="sr-only">Open main menu</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile menu -->
  {#if mobileMenuOpen}
    <div class="mobile-menu sm:hidden">
      <div class="space-y-1 border-t border-gray-200 pb-3 pt-2">
        {#if isAuthenticated}
          <a
            href="/dashboard"
            class="block border-l-4 py-2 pl-3 pr-4 text-base font-medium
              {isCurrentPath('/dashboard') 
                ? 'border-blue-500 bg-blue-50 text-blue-700' 
                : 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800'}"
            on:click={closeMobileMenu}
          >
            Dashboard
          </a>
          <a
            href="/issues"
            class="block border-l-4 py-2 pl-3 pr-4 text-base font-medium
              {isCurrentPath('/issues') 
                ? 'border-blue-500 bg-blue-50 text-blue-700' 
                : 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800'}"
            on:click={closeMobileMenu}
          >
            Issues
          </a>
          <a
            href="/issues/create"
            class="block border-l-4 py-2 pl-3 pr-4 text-base font-medium
              {isCurrentPath('/issues/create') 
                ? 'border-blue-500 bg-blue-50 text-blue-700' 
                : 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800'}"
            on:click={closeMobileMenu}
          >
            Create Issue
          </a>
          {#if user?.role === 'ADMIN'}
            <a
              href="/admin"
              class="block border-l-4 py-2 pl-3 pr-4 text-base font-medium
                {isCurrentPath('/admin') 
                  ? 'border-blue-500 bg-blue-50 text-blue-700' 
                  : 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800'}"
              on:click={closeMobileMenu}
            >
              Admin
            </a>
          {/if}
        {/if}
      </div>
      
      {#if isAuthenticated && user}
        <div class="border-t border-gray-200 pb-3 pt-4">
          <div class="flex items-center px-4">
            <div class="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
              {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{user.name || user.email}</div>
              <div class="text-sm font-medium text-gray-500 capitalize">{user.role.toLowerCase()}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <a
              href="/profile"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
              on:click={closeMobileMenu}
            >
              Your Profile
            </a>
            <a
              href="/settings"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
              on:click={closeMobileMenu}
            >
              Settings
            </a>
            <button
              type="button"
              class="block w-full px-4 py-2 text-left text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
              on:click={handleLogout}
            >
              Sign out
            </button>
          </div>
        </div>
      {:else}
        <div class="border-t border-gray-200 pb-3 pt-4">
          <div class="space-y-1">
            <a
              href="/auth/login"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
              on:click={closeMobileMenu}
            >
              Sign in
            </a>
            <a
              href="/auth/register"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
              on:click={closeMobileMenu}
            >
              Sign up
            </a>
          </div>
        </div>
      {/if}
    </div>
  {/if}
</nav>