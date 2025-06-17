/**
 * Genesis Engine WebSocket Client
 * Real-time communication for the Genesis Agentic Development Engine
 */

import { io, Socket } from 'socket.io-client';
import { config } from './config';
import type { WebSocketMessage, WebSocketState } from '@/types';

type EventCallback = (data: any) => void;
type EventMap = Record<string, EventCallback[]>;

class WebSocketClient {
  private socket: Socket | null = null;
  private eventMap: EventMap = {};
  private state: WebSocketState = {
    connected: false,
    reconnecting: false,
    reconnectAttempts: 0,
  };
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;

  constructor() {
    this.connect();
  }

  /**
   * Connect to the WebSocket server
   */
  connect(): void {
    if (this.socket?.connected) {
      return;
    }

    try {
      this.socket = io(config.websocket.url, {
        transports: ['websocket', 'polling'],
        timeout: 20000,
        reconnection: false, // We'll handle reconnection manually
        auth: {
          token: this.getAuthToken(),
        },
      });

      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      this.scheduleReconnect();
    }
  }

  /**
   * Disconnect from the WebSocket server
   */
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }

    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }

    this.updateState({
      connected: false,
      reconnecting: false,
      lastDisconnected: new Date(),
    });
  }

  /**
   * Setup event listeners for the socket
   */
  private setupEventListeners(): void {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.updateState({
        connected: true,
        reconnecting: false,
        reconnectAttempts: 0,
        lastConnected: new Date(),
      });

      this.startHeartbeat();
      this.emit('connection', { status: 'connected' });
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
      this.updateState({
        connected: false,
        lastDisconnected: new Date(),
      });

      this.stopHeartbeat();
      this.emit('connection', { status: 'disconnected', reason });

      // Auto-reconnect unless it was a manual disconnect
      if (reason !== 'io client disconnect') {
        this.scheduleReconnect();
      }
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.emit('error', { type: 'connection_error', error });
      this.scheduleReconnect();
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', { type: 'socket_error', error });
    });

    // Handle authentication errors
    this.socket.on('auth_error', (error) => {
      console.error('WebSocket authentication error:', error);
      this.emit('auth_error', error);
      // Don't reconnect on auth errors
    });

    // Handle custom events
    this.socket.on('message', (data: WebSocketMessage) => {
      this.handleMessage(data);
    });

    // Agent-specific events
    this.socket.on('agent_status', (data) => {
      this.emit('agent_status', data);
    });

    this.socket.on('task_update', (data) => {
      this.emit('task_update', data);
    });

    this.socket.on('code_generation', (data) => {
      this.emit('code_generation', data);
    });

    this.socket.on('collaboration', (data) => {
      this.emit('collaboration', data);
    });

    this.socket.on('notification', (data) => {
      this.emit('notification', data);
    });
  }

  /**
   * Handle incoming messages
   */
  private handleMessage(message: WebSocketMessage): void {
    if (config.development.enableDebugMode) {
      console.log('WebSocket message received:', message);
    }

    this.emit('message', message);
    
    // Emit specific event type if available
    if (message.type) {
      this.emit(message.type, message.payload);
    }
  }

  /**
   * Schedule a reconnection attempt
   */
  private scheduleReconnect(): void {
    if (this.state.reconnectAttempts >= config.websocket.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('max_reconnect_attempts', { attempts: this.state.reconnectAttempts });
      return;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.updateState({
      reconnecting: true,
      reconnectAttempts: this.state.reconnectAttempts + 1,
    });

    const delay = Math.min(
      config.websocket.reconnectInterval * Math.pow(2, this.state.reconnectAttempts),
      30000 // Max 30 seconds
    );

    console.log(`Scheduling reconnection attempt ${this.state.reconnectAttempts} in ${delay}ms`);
    
    this.reconnectTimer = setTimeout(() => {
      this.connect();
    }, delay);
  }

  /**
   * Start heartbeat to keep connection alive
   */
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.socket?.connected) {
        this.socket.emit('ping');
      }
    }, config.agents.heartbeatInterval);
  }

  /**
   * Stop heartbeat
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /**
   * Get authentication token
   */
  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('genesis_auth_token');
    }
    return null;
  }

  /**
   * Update WebSocket state
   */
  private updateState(updates: Partial<WebSocketState>): void {
    this.state = { ...this.state, ...updates };
    this.emit('state_change', this.state);
  }

  /**
   * Send a message to the server
   */
  send(event: string, data?: any): void {
    if (!this.socket?.connected) {
      console.warn('WebSocket not connected, message not sent:', { event, data });
      return;
    }

    this.socket.emit(event, data);
  }

  /**
   * Subscribe to an event
   */
  on(event: string, callback: EventCallback): void {
    if (!this.eventMap[event]) {
      this.eventMap[event] = [];
    }
    this.eventMap[event].push(callback);
  }

  /**
   * Unsubscribe from an event
   */
  off(event: string, callback?: EventCallback): void {
    if (!this.eventMap[event]) return;

    if (callback) {
      this.eventMap[event] = this.eventMap[event].filter(cb => cb !== callback);
    } else {
      delete this.eventMap[event];
    }
  }

  /**
   * Emit an event to all subscribers
   */
  private emit(event: string, data?: any): void {
    if (!this.eventMap[event]) return;

    this.eventMap[event].forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in WebSocket event handler for ${event}:`, error);
      }
    });
  }

  /**
   * Get current connection state
   */
  getState(): WebSocketState {
    return { ...this.state };
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.state.connected;
  }

  /**
   * Join a room (for collaboration features)
   */
  joinRoom(roomId: string): void {
    this.send('join_room', { room_id: roomId });
  }

  /**
   * Leave a room
   */
  leaveRoom(roomId: string): void {
    this.send('leave_room', { room_id: roomId });
  }

  /**
   * Send a collaboration event
   */
  sendCollaboration(data: any): void {
    this.send('collaboration', data);
  }

  /**
   * Request agent status
   */
  requestAgentStatus(agentId?: string): void {
    this.send('get_agent_status', { agent_id: agentId });
  }

  /**
   * Subscribe to task updates
   */
  subscribeToTask(taskId: string): void {
    this.send('subscribe_task', { task_id: taskId });
  }

  /**
   * Unsubscribe from task updates
   */
  unsubscribeFromTask(taskId: string): void {
    this.send('unsubscribe_task', { task_id: taskId });
  }
}

// Export singleton instance
export const wsClient = new WebSocketClient();
export default wsClient;