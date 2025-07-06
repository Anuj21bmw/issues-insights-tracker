// frontend/src/lib/stores/toast.ts

import { writable } from 'svelte/store';

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
}

function createToastStore() {
  const { subscribe, update } = writable<Toast[]>([]);

  function addToast(toast: Omit<Toast, 'id'>) {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast: Toast = {
      id,
      duration: 5000,
      ...toast
    };

    update(toasts => [...toasts, newToast]);

    // Auto remove after duration
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

  return {
    subscribe,
    // Fixed: Add the missing 'add' method
    add: addToast,
    // Function overloads to support both single and double parameters
    success: (title: string, message: string = '', duration: number = 5000) => 
      addToast({ type: 'success', title, message, duration }),
    error: (title: string, message: string = '', duration: number = 5000) => 
      addToast({ type: 'error', title, message, duration }),
    warning: (title: string, message: string = '', duration: number = 5000) => 
      addToast({ type: 'warning', title, message, duration }),
    info: (title: string, message: string = '', duration: number = 5000) => 
      addToast({ type: 'info', title, message, duration }),
    remove: removeToast,
    clear: () => update(() => [])
  };
}

export const toastStore = createToastStore();

// Export default toasts for easier access
export const toasts = toastStore;