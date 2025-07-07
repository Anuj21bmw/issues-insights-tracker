import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'light' | 'dark';

const initial: Theme = browser && localStorage.getItem('theme') === 'dark' ? 'dark' : 'light';

const store = writable<Theme>(initial);

if (browser) {
  document.documentElement.classList.toggle('dark-mode', initial === 'dark');
}

function setTheme(value: Theme) {
  store.set(value);
  if (browser) {
    localStorage.setItem('theme', value);
    document.documentElement.classList.toggle('dark-mode', value === 'dark');
  }
}

function toggle() {
  store.update((value) => {
    const next = value === 'dark' ? 'light' : 'dark';
    if (browser) {
      localStorage.setItem('theme', next);
      document.documentElement.classList.toggle('dark-mode', next === 'dark');
    }
    return next;
  });
}

export const theme = {
  subscribe: store.subscribe,
  set: setTheme,
  toggle
};
