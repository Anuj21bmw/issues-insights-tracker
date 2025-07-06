// frontend/src/lib/stores/auth.ts

import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';

export interface User {
  id: string;
  email: string;
  role: 'ADMIN' | 'MAINTAINER' | 'REPORTER';
  name?: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  loading: false
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  const API_BASE = 'http://localhost:8000';

  return {
    subscribe,
    
    async initAuth() {
      if (!browser) return;
      
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      
      try {
        update(state => ({ ...state, loading: true }));
        
        const response = await fetch(`${API_BASE}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const user = await response.json();
          set({
            isAuthenticated: true,
            user,
            token,
            loading: false
          });
        } else {
          localStorage.removeItem('auth_token');
          set(initialState);
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        localStorage.removeItem('auth_token');
        set(initialState);
      }
    },
    
    async login(email: string, password: string) {
      try {
        update(state => ({ ...state, loading: true }));
        
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE}/api/auth/login`, {
          method: 'POST',
          body: formData
        });
        
        if (response.ok) {
          const { access_token } = await response.json();
          
          // Get user info
          const userResponse = await fetch(`${API_BASE}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${access_token}`
            }
          });
          
          if (userResponse.ok) {
            const user = await userResponse.json();
            
            if (browser) {
              localStorage.setItem('auth_token', access_token);
            }
            
            set({
              isAuthenticated: true,
              user,
              token: access_token,
              loading: false
            });
            
            goto('/dashboard');
            return { success: true };
          }
        }
        
        const error = await response.json();
        update(state => ({ ...state, loading: false }));
        return { success: false, error: error.detail || 'Login failed' };
        
      } catch (error) {
        console.error('Login error:', error);
        update(state => ({ ...state, loading: false }));
        return { success: false, error: 'Network error' };
      }
    },
    
    async register(userData: { name: string; email: string; password: string; role?: string }) {
      try {
        update(state => ({ ...state, loading: true }));
        
        const response = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...userData,
            role: userData.role || 'REPORTER'
          })
        });
        
        if (response.ok) {
          const { access_token } = await response.json();
          
          // Get user info
          const userResponse = await fetch(`${API_BASE}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${access_token}`
            }
          });
          
          if (userResponse.ok) {
            const user = await userResponse.json();
            
            if (browser) {
              localStorage.setItem('auth_token', access_token);
            }
            
            set({
              isAuthenticated: true,
              user,
              token: access_token,
              loading: false
            });
            
            goto('/dashboard');
            return { success: true };
          }
        }
        
        const error = await response.json();
        update(state => ({ ...state, loading: false }));
        return { success: false, error: error.detail || 'Registration failed' };
        
      } catch (error) {
        console.error('Registration error:', error);
        update(state => ({ ...state, loading: false }));
        return { success: false, error: 'Network error' };
      }
    },
    
    logout() {
      if (browser) {
        localStorage.removeItem('auth_token');
      }
      set(initialState);
      goto('/auth/login');
    },
    
    hasRole(role: string): boolean {
      const state = this.getCurrentState();
      if (!state.user) return false;
      
      const roleHierarchy = {
        'ADMIN': 3,
        'MAINTAINER': 2,
        'REPORTER': 1
      };
      
      const userLevel = roleHierarchy[state.user.role as keyof typeof roleHierarchy] || 0;
      const requiredLevel = roleHierarchy[role as keyof typeof roleHierarchy] || 0;
      
      return userLevel >= requiredLevel;
    },
    
    getCurrentState(): AuthState {
      let currentState: AuthState = initialState;
      this.subscribe(state => currentState = state)();
      return currentState;
    }
  };
}

export const authStore = createAuthStore();