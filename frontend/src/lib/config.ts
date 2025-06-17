/**
 * Genesis Engine Frontend Configuration
 * Centralized configuration for the Genesis Agentic Development Engine
 */

export const config = {
  // API Configuration
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 30000,
    retries: 3,
  },

  // WebSocket Configuration
  websocket: {
    url: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws',
    reconnectInterval: 5000,
    maxReconnectAttempts: 10,
  },

  // Agent Configuration
  agents: {
    maxConcurrentTasks: 5,
    taskTimeout: 300000, // 5 minutes
    heartbeatInterval: 30000,
  },

  // UI Configuration
  ui: {
    theme: {
      defaultMode: 'system' as 'light' | 'dark' | 'system',
      enableAnimations: true,
    },
    editor: {
      fontSize: 14,
      tabSize: 2,
      wordWrap: true,
      minimap: true,
    },
  },

  // Development Configuration
  development: {
    enableDebugMode: process.env.NODE_ENV === 'development',
    enablePerformanceMonitoring: true,
    enableErrorBoundaries: true,
  },

  // Feature Flags
  features: {
    enableRealTimeCollaboration: true,
    enableAICodeGeneration: true,
    enableMultiAgentOrchestration: true,
    enableAdvancedDebugging: true,
  },
} as const;

export type Config = typeof config;