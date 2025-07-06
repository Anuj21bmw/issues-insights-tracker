// src/lib/stores/auth.ts

import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { User } from '$lib/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
}

function createAuthStore() {
  const initialState: AuthState = {
    user: null,
    isAuthenticated: false,
    isLoading: true,
    token: null
  };

  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    
    // Initialize auth state from localStorage
    init: async () => {
      if (!browser) {
        set({ ...initialState, isLoading: false });
        return;
      }
      
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          // Verify token and get user info
          const response = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            const user = await response.json();
            set({
              user,
              isAuthenticated: true,
              isLoading: false,
              token
            });
          } else {
            // Token is invalid, clear it
            localStorage.removeItem('access_token');
            set({
              user: null,
              isAuthenticated: false,
              isLoading: false,
              token: null
            });
          }
        } catch (error) {
          console.error('Auth initialization error:', error);
          localStorage.removeItem('access_token');
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            token: null
          });
        }
      } else {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          token: null
        });
      }
    },

    // Login with email and password
    login: async (email: string, password: string) => {
      try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch('http://localhost:8000/api/auth/login', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          const token = data.access_token;
          
          if (browser) {
            localStorage.setItem('access_token', token);
          }
          
          // Get user info
          const userResponse = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (userResponse.ok) {
            const user = await userResponse.json();
            set({
              user,
              isAuthenticated: true,
              isLoading: false,
              token
            });
            return { success: true, user };
          }
        }
        
        const errorData = await response.json();
        return { 
          success: false, 
          error: errorData.detail || 'Login failed' 
        };
      } catch (error) {
        return { 
          success: false, 
          error: 'Network error. Please try again.' 
        };
      }
    },

    // Register new user
    register: async (userData: { name: string; email: string; password: string; role?: string }) => {
      try {
        const response = await fetch('http://localhost:8000/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: userData.name,
            email: userData.email,
            password: userData.password,
            role: userData.role || 'REPORTER'
          })
        });

        if (response.ok) {
          const data = await response.json();
          const token = data.access_token;
          
          if (browser) {
            localStorage.setItem('access_token', token);
          }
          
          // Get user info
          const userResponse = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (userResponse.ok) {
            const user = await userResponse.json();
            set({
              user,
              isAuthenticated: true,
              isLoading: false,
              token
            });
            return { success: true, user };
          }
        }
        
        const errorData = await response.json();
        return { 
          success: false, 
          error: errorData.detail || 'Registration failed' 
        };
      } catch (error) {
        return { 
          success: false, 
          error: 'Network error. Please try again.' 
        };
      }
    },

    // Logout user
    logout: () => {
      if (browser) {
        localStorage.removeItem('access_token');
      }
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        token: null
      });
    },

    // Update user info
    updateUser: (userData: Partial<User>) => {
      update(state => ({
        ...state,
        user: state.user ? { ...state.user, ...userData } : null
      }));
    },

    // Set loading state
    setLoading: (loading: boolean) => {
      update(state => ({
        ...state,
        isLoading: loading
      }));
    }
  };
}

export const authStore = createAuthStore();