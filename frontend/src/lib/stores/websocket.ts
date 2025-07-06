// frontend/src/lib/stores/websocket.ts

import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { toastStore } from './toast';

interface WebSocketMessage {
  type: string;
  data?: any;
  timestamp?: string;
  updated_by?: string;
  issue_id?: string;
  deleted_by?: string;
}

interface WebSocketState {
  connected: boolean;
  connecting: boolean;
  lastMessage: WebSocketMessage | null;
  connectionCount: number;
}

const initialState: WebSocketState = {
  connected: false,
  connecting: false,
  lastMessage: null,
  connectionCount: 0
};

function createWebSocketStore() {
  const { subscribe, set, update } = writable<WebSocketState>(initialState);
  
  let ws: WebSocket | null = null;
  let reconnectTimeout: NodeJS.Timeout | null = null;
  let reconnectAttempts = 0;
  const maxReconnectAttempts = 5;
  const reconnectDelay = 5000; // 5 seconds
  
  const WS_URL = 'ws://localhost:8000/ws';
  
  return {
    subscribe,
    
    connect(token?: string) {
      if (!browser || ws?.readyState === WebSocket.OPEN) return;
      
      update(state => ({ ...state, connecting: true }));
      
      const wsUrl = token ? `${WS_URL}?token=${token}` : WS_URL;
      
      try {
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
          console.log('WebSocket connected');
          reconnectAttempts = 0;
          update(state => ({
            ...state,
            connected: true,
            connecting: false
          }));
          
          // Send ping every 30 seconds to keep connection alive
          const pingInterval = setInterval(() => {
            if (ws?.readyState === WebSocket.OPEN) {
              ws.send('ping');
            } else {
              clearInterval(pingInterval);
            }
          }, 30000);
        };
        
        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            
            update(state => ({
              ...state,
              lastMessage: message
            }));
            
            // Handle different message types
            handleMessage(message);
            
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };
        
        ws.onclose = (event) => {
          console.log('WebSocket disconnected:', event.code, event.reason);
          update(state => ({
            ...state,
            connected: false,
            connecting: false
          }));
          
          // Attempt to reconnect if not intentionally closed
          if (event.code !== 1000 && reconnectAttempts < maxReconnectAttempts) {
            scheduleReconnect(token);
          }
        };
        
        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          update(state => ({
            ...state,
            connected: false,
            connecting: false
          }));
        };
        
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
        update(state => ({
          ...state,
          connecting: false
        }));
      }
    },
    
    disconnect() {
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
      }
      
      if (ws) {
        ws.close(1000, 'User disconnected');
        ws = null;
      }
      
      set(initialState);
    },
    
    sendMessage(message: any) {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
      }
    }
  };
  
  function handleMessage(message: WebSocketMessage) {
    switch (message.type) {
      case 'connected':
        toastStore.success('Connected to real-time updates');
        break;
        
      case 'issue_created':
        toastStore.info('New issue created');
        // Dispatch custom event for issue list to refresh
        if (browser) {
          window.dispatchEvent(new CustomEvent('issue-created', { detail: message.data }));
        }
        break;
        
      case 'issue_updated':
        toastStore.info(`Issue updated by ${message.updated_by}`);
        if (browser) {
          window.dispatchEvent(new CustomEvent('issue-updated', { detail: message.data }));
        }
        break;
        
      case 'issue_deleted':
        toastStore.warning(`Issue deleted by ${message.deleted_by}`);
        if (browser) {
          window.dispatchEvent(new CustomEvent('issue-deleted', { detail: { id: message.issue_id } }));
        }
        break;
        
      default:
        console.log('Unknown WebSocket message type:', message.type);
    }
  }
  
  function scheduleReconnect(token?: string) {
    reconnectAttempts++;
    const delay = reconnectDelay * Math.pow(2, reconnectAttempts - 1); // Exponential backoff
    
    console.log(`Scheduling reconnect attempt ${reconnectAttempts} in ${delay}ms`);
    
    reconnectTimeout = setTimeout(() => {
      console.log(`Attempting to reconnect (${reconnectAttempts}/${maxReconnectAttempts})`);
      websocketStore.connect(token);
    }, delay);
  }
}

export const websocketStore = createWebSocketStore();