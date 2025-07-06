// src/lib/stores/toast.ts 
import { writable } from 'svelte/store';

// Export the Toast interface
export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

function createToastStore() {
  const { subscribe, update } = writable<Toast[]>([]);

  function addToast(toast: Omit<Toast, 'id'>) {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration || 5000
    };

    update(toasts => [...toasts, newToast]);

    // Auto remove toast after duration
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, newToast.duration);
    }

    return id;
  }

  function removeToast(id: string) {
    update(toasts => toasts.filter(toast => toast.id !== id));
  }

  function clearAll() {
    update(() => []);
  }

  return {
    subscribe,
    
    // Convenience methods
    success: (message: string, duration?: number) => 
      addToast({ type: 'success', message, duration }),
    
    error: (message: string, duration?: number) => 
      addToast({ type: 'error', message, duration }),
    
    warning: (message: string, duration?: number) => 
      addToast({ type: 'warning', message, duration }),
    
    info: (message: string, duration?: number) => 
      addToast({ type: 'info', message, duration }),
    
    // Core methods
    add: addToast,
    remove: removeToast,
    clear: clearAll
  };
}

export const toastStore = createToastStore();