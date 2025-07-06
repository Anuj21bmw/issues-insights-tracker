// src/lib/stores/auth.ts
import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { AuthState, User } from '$lib/types';

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  loading: false
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    
    // Initialize auth state from localStorage
    init: () => {
      if (browser) {
        const token = localStorage.getItem('auth_token');
        const userStr = localStorage.getItem('auth_user');
        
        if (token && userStr) {
          try {
            const user = JSON.parse(userStr);
            set({
              isAuthenticated: true,
              user,
              token,
              loading: false
            });
          } catch (error) {
            console.error('Failed to parse stored user data:', error);
            // Clear invalid data
            localStorage.removeItem('auth_token');
            localStorage.removeItem('auth_user');
          }
        }
      }
    },

    // Set loading state
    setLoading: (loading: boolean) => {
      update(state => ({ ...state, loading }));
    },

    // Login user
    login: (token: string, user: User) => {
      if (browser) {
        localStorage.setItem('auth_token', token);
        localStorage.setItem('auth_user', JSON.stringify(user));
      }
      
      set({
        isAuthenticated: true,
        user,
        token,
        loading: false
      });
    },

    // Update user info
    updateUser: (user: User) => {
      if (browser) {
        localStorage.setItem('auth_user', JSON.stringify(user));
      }
      
      update(state => ({
        ...state,
        user
      }));
    },

    // Logout user
    logout: () => {
      if (browser) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
      
      set({
        isAuthenticated: false,
        user: null,
        token: null,
        loading: false
      });
    },

    // Clear auth state (for errors)
    clear: () => {
      if (browser) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
      set(initialState);
    }
  };
}

export const authStore = createAuthStore();