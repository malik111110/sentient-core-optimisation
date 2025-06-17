# Core Framework Integration Guide

**ID:** guide:feature:core_framework_integration  
**Source Reference(s):** /agentic web dev/core  
**Last Validated:** January 2025

## 1. Purpose

Implement the Core framework for building modern web applications with integrated AI capabilities, providing a foundation for rapid development, component reusability, and seamless AI agent integration within the Genesis Engine.

## 2. Key Concepts

- **Component Architecture**: Modular, reusable UI components with built-in AI integration
- **State Management**: Centralized state management with real-time synchronization
- **AI Integration**: Native AI agent communication and task delegation
- **Hot Reloading**: Development-time hot module replacement and live updates
- **Type Safety**: Full TypeScript support with strict type checking
- **Plugin System**: Extensible plugin architecture for custom functionality
- **Performance Optimization**: Built-in performance monitoring and optimization
- **Developer Experience**: Enhanced development tools and debugging capabilities

## 3. Required Dependencies

### Frontend Dependencies
```json
{
  "dependencies": {
    "@core/framework": "^2.0.0",
    "@core/components": "^2.0.0",
    "@core/state": "^2.0.0",
    "@core/ai": "^2.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "framer-motion": "^10.16.0",
    "zustand": "^4.4.0",
    "react-query": "^3.39.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.0.0",
    "clsx": "^2.0.0",
    "class-variance-authority": "^0.7.0"
  },
  "devDependencies": {
    "@core/dev-tools": "^2.0.0",
    "@types/node": "^20.10.0",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0",
    "prettier": "^3.1.0",
    "vitest": "^1.1.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jsdom": "^23.0.0"
  }
}
```

### Environment Variables
```bash
# Core Framework Configuration
CORE_ENVIRONMENT=development
CORE_DEBUG=true
CORE_LOG_LEVEL=debug
CORE_HOT_RELOAD=true

# AI Integration
CORE_AI_ENDPOINT=http://localhost:8000/api/ai
CORE_AI_WEBSOCKET=ws://localhost:8000/ws
CORE_AI_API_KEY=your_ai_api_key
CORE_AI_TIMEOUT=30000

# State Management
CORE_STATE_PERSISTENCE=true
CORE_STATE_SYNC_INTERVAL=1000
CORE_STATE_COMPRESSION=true

# Performance
CORE_BUNDLE_ANALYZER=false
CORE_PERFORMANCE_MONITORING=true
CORE_LAZY_LOADING=true
CORE_CODE_SPLITTING=true

# Development
CORE_DEV_SERVER_PORT=3000
CORE_DEV_SERVER_HOST=localhost
CORE_SOURCE_MAPS=true
CORE_TYPE_CHECKING=true

# Build Configuration
CORE_BUILD_TARGET=es2020
CORE_BUILD_MINIFY=true
CORE_BUILD_TREESHAKE=true
CORE_BUILD_OUTPUT_DIR=dist

# Security
CORE_CSP_ENABLED=true
CORE_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
CORE_SECURE_COOKIES=false

# Analytics and Monitoring
CORE_ANALYTICS_ENABLED=false
CORE_ERROR_REPORTING=true
CORE_PERFORMANCE_BUDGET={
  "maxAssetSize": 250000,
  "maxEntrypointSize": 250000
}
```

## 4. Step-by-Step Implementation Plan

### 4.1 Project Setup and Configuration
1. Initialize Core framework project structure
2. Configure build system and development tools
3. Set up TypeScript configuration and type definitions
4. Configure styling system (Tailwind CSS)
5. Set up testing framework and utilities

### 4.2 Component Architecture Implementation
1. Create base component library and design system
2. Implement component composition patterns
3. Set up component documentation and storybook
4. Create reusable UI primitives and layouts
5. Implement accessibility features and ARIA support

### 4.3 State Management Setup
1. Configure centralized state management (Zustand)
2. Implement state persistence and hydration
3. Set up real-time state synchronization
4. Create state management patterns and best practices
5. Implement optimistic updates and conflict resolution

### 4.4 AI Integration Layer
1. Set up AI agent communication protocols
2. Implement AI task delegation and result handling
3. Create AI-powered component behaviors
4. Set up real-time AI interaction streams
5. Implement AI context and conversation management

### 4.5 Development Experience Enhancement
1. Configure hot module replacement and live reloading
2. Set up development tools and debugging utilities
3. Implement error boundaries and error reporting
4. Create development-time performance monitoring
5. Set up automated testing and quality assurance

## 5. Core Code Example

### 5.1 Core Framework Configuration
```typescript
// src/config/core.config.ts
import { CoreConfig } from '@core/framework';

export const coreConfig: CoreConfig = {
  // Environment configuration
  environment: process.env.CORE_ENVIRONMENT as 'development' | 'production' | 'test',
  debug: process.env.CORE_DEBUG === 'true',
  logLevel: process.env.CORE_LOG_LEVEL as 'debug' | 'info' | 'warn' | 'error',
  
  // Development configuration
  hotReload: process.env.CORE_HOT_RELOAD === 'true',
  devServer: {
    port: parseInt(process.env.CORE_DEV_SERVER_PORT || '3000'),
    host: process.env.CORE_DEV_SERVER_HOST || 'localhost',
    sourceMaps: process.env.CORE_SOURCE_MAPS === 'true',
  },
  
  // AI integration configuration
  ai: {
    endpoint: process.env.CORE_AI_ENDPOINT || 'http://localhost:8000/api/ai',
    websocket: process.env.CORE_AI_WEBSOCKET || 'ws://localhost:8000/ws',
    apiKey: process.env.CORE_AI_API_KEY,
    timeout: parseInt(process.env.CORE_AI_TIMEOUT || '30000'),
    retryAttempts: 3,
    retryDelay: 1000,
  },
  
  // State management configuration
  state: {
    persistence: process.env.CORE_STATE_PERSISTENCE === 'true',
    syncInterval: parseInt(process.env.CORE_STATE_SYNC_INTERVAL || '1000'),
    compression: process.env.CORE_STATE_COMPRESSION === 'true',
    storageKey: 'core-app-state',
  },
  
  // Performance configuration
  performance: {
    monitoring: process.env.CORE_PERFORMANCE_MONITORING === 'true',
    lazyLoading: process.env.CORE_LAZY_LOADING === 'true',
    codeSplitting: process.env.CORE_CODE_SPLITTING === 'true',
    bundleAnalyzer: process.env.CORE_BUNDLE_ANALYZER === 'true',
  },
  
  // Build configuration
  build: {
    target: process.env.CORE_BUILD_TARGET || 'es2020',
    minify: process.env.CORE_BUILD_MINIFY === 'true',
    treeshake: process.env.CORE_BUILD_TREESHAKE === 'true',
    outputDir: process.env.CORE_BUILD_OUTPUT_DIR || 'dist',
  },
  
  // Security configuration
  security: {
    csp: process.env.CORE_CSP_ENABLED === 'true',
    corsOrigins: process.env.CORE_CORS_ORIGINS?.split(',') || [],
    secureCookies: process.env.CORE_SECURE_COOKIES === 'true',
  },
};
```

### 5.2 Core Application Setup
```typescript
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { CoreProvider, createCoreApp } from '@core/framework';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';

import { coreConfig } from './config/core.config';
import { AppStateProvider } from './store/app-state';
import { AIProvider } from './providers/ai-provider';
import { App } from './App';
import './styles/globals.css';

// Create Core application instance
const coreApp = createCoreApp(coreConfig);

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

// Initialize application
const initializeApp = async () => {
  try {
    // Initialize Core framework
    await coreApp.initialize();
    
    // Setup error reporting
    if (coreConfig.performance.monitoring) {
      await coreApp.setupErrorReporting();
    }
    
    // Setup performance monitoring
    if (coreConfig.performance.monitoring) {
      await coreApp.setupPerformanceMonitoring();
    }
    
    console.log('Core application initialized successfully');
  } catch (error) {
    console.error('Failed to initialize Core application:', error);
  }
};

// Render application
const renderApp = () => {
  const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
  );
  
  root.render(
    <React.StrictMode>
      <CoreProvider app={coreApp}>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppStateProvider>
              <AIProvider>
                <App />
              </AIProvider>
            </AppStateProvider>
          </BrowserRouter>
        </QueryClientProvider>
      </CoreProvider>
    </React.StrictMode>
  );
};

// Initialize and render
initializeApp().then(renderApp);

// Hot module replacement
if (import.meta.hot && coreConfig.hotReload) {
  import.meta.hot.accept('./App', () => {
    renderApp();
  });
}
```

### 5.3 State Management Implementation
```typescript
// src/store/app-state.tsx
import React, { createContext, useContext, ReactNode } from 'react';
import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { devtools } from 'zustand/middleware';

// State interfaces
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  preferences: UserPreferences;
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  notifications: boolean;
  aiAssistance: boolean;
}

interface AIState {
  isConnected: boolean;
  currentConversation?: string;
  conversations: Record<string, Conversation>;
  agents: Record<string, AIAgent>;
  tasks: Record<string, AITask>;
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  agentId?: string;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  metadata?: Record<string, any>;
}

interface AIAgent {
  id: string;
  name: string;
  description: string;
  capabilities: string[];
  status: 'online' | 'offline' | 'busy';
  avatar?: string;
}

interface AITask {
  id: string;
  type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  result?: any;
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  loading: boolean;
  notifications: Notification[];
  modals: Record<string, boolean>;
}

interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  actions?: NotificationAction[];
}

interface NotificationAction {
  label: string;
  action: () => void;
  variant?: 'primary' | 'secondary';
}

// Main application state
interface AppState {
  // User state
  user: User | null;
  isAuthenticated: boolean;
  
  // AI state
  ai: AIState;
  
  // UI state
  ui: UIState;
  
  // Actions
  setUser: (user: User | null) => void;
  updateUserPreferences: (preferences: Partial<UserPreferences>) => void;
  
  // AI actions
  setAIConnection: (connected: boolean) => void;
  addConversation: (conversation: Conversation) => void;
  updateConversation: (id: string, updates: Partial<Conversation>) => void;
  addMessage: (conversationId: string, message: Message) => void;
  setCurrentConversation: (id: string | undefined) => void;
  updateAgent: (id: string, updates: Partial<AIAgent>) => void;
  addTask: (task: AITask) => void;
  updateTask: (id: string, updates: Partial<AITask>) => void;
  
  // UI actions
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setLoading: (loading: boolean) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  markNotificationRead: (id: string) => void;
  removeNotification: (id: string) => void;
  setModal: (modalId: string, open: boolean) => void;
}

// Create Zustand store
const useAppStore = create<AppState>()()
  devtools(
    persist(
      subscribeWithSelector(
        immer((set, get) => ({
          // Initial state
          user: null,
          isAuthenticated: false,
          
          ai: {
            isConnected: false,
            conversations: {},
            agents: {},
            tasks: {},
          },
          
          ui: {
            sidebarOpen: true,
            theme: 'light',
            loading: false,
            notifications: [],
            modals: {},
          },
          
          // User actions
          setUser: (user) => {
            set((state) => {
              state.user = user;
              state.isAuthenticated = !!user;
            });
          },
          
          updateUserPreferences: (preferences) => {
            set((state) => {
              if (state.user) {
                Object.assign(state.user.preferences, preferences);
              }
            });
          },
          
          // AI actions
          setAIConnection: (connected) => {
            set((state) => {
              state.ai.isConnected = connected;
            });
          },
          
          addConversation: (conversation) => {
            set((state) => {
              state.ai.conversations[conversation.id] = conversation;
            });
          },
          
          updateConversation: (id, updates) => {
            set((state) => {
              if (state.ai.conversations[id]) {
                Object.assign(state.ai.conversations[id], updates);
                state.ai.conversations[id].updatedAt = new Date();
              }
            });
          },
          
          addMessage: (conversationId, message) => {
            set((state) => {
              if (state.ai.conversations[conversationId]) {
                state.ai.conversations[conversationId].messages.push(message);
                state.ai.conversations[conversationId].updatedAt = new Date();
              }
            });
          },
          
          setCurrentConversation: (id) => {
            set((state) => {
              state.ai.currentConversation = id;
            });
          },
          
          updateAgent: (id, updates) => {
            set((state) => {
              if (state.ai.agents[id]) {
                Object.assign(state.ai.agents[id], updates);
              } else {
                state.ai.agents[id] = updates as AIAgent;
              }
            });
          },
          
          addTask: (task) => {
            set((state) => {
              state.ai.tasks[task.id] = task;
            });
          },
          
          updateTask: (id, updates) => {
            set((state) => {
              if (state.ai.tasks[id]) {
                Object.assign(state.ai.tasks[id], updates);
                state.ai.tasks[id].updatedAt = new Date();
              }
            });
          },
          
          // UI actions
          setSidebarOpen: (open) => {
            set((state) => {
              state.ui.sidebarOpen = open;
            });
          },
          
          setTheme: (theme) => {
            set((state) => {
              state.ui.theme = theme;
              if (state.user) {
                state.user.preferences.theme = theme;
              }
            });
          },
          
          setLoading: (loading) => {
            set((state) => {
              state.ui.loading = loading;
            });
          },
          
          addNotification: (notification) => {
            set((state) => {
              const newNotification: Notification = {
                ...notification,
                id: `notification-${Date.now()}-${Math.random()}`,
                timestamp: new Date(),
                read: false,
              };
              state.ui.notifications.unshift(newNotification);
              
              // Keep only last 50 notifications
              if (state.ui.notifications.length > 50) {
                state.ui.notifications = state.ui.notifications.slice(0, 50);
              }
            });
          },
          
          markNotificationRead: (id) => {
            set((state) => {
              const notification = state.ui.notifications.find(n => n.id === id);
              if (notification) {
                notification.read = true;
              }
            });
          },
          
          removeNotification: (id) => {
            set((state) => {
              state.ui.notifications = state.ui.notifications.filter(n => n.id !== id);
            });
          },
          
          setModal: (modalId, open) => {
            set((state) => {
              state.ui.modals[modalId] = open;
            });
          },
        }))
      ),
      {
        name: 'core-app-state',
        partialize: (state) => ({
          user: state.user,
          ai: {
            conversations: state.ai.conversations,
            agents: state.ai.agents,
          },
          ui: {
            theme: state.ui.theme,
            sidebarOpen: state.ui.sidebarOpen,
          },
        }),
      }
    ),
    {
      name: 'core-app-store',
    }
  )
);

// Context for providing store
const AppStateContext = createContext<typeof useAppStore | null>(null);

// Provider component
interface AppStateProviderProps {
  children: ReactNode;
}

export const AppStateProvider: React.FC<AppStateProviderProps> = ({ children }) => {
  return (
    <AppStateContext.Provider value={useAppStore}>
      {children}
    </AppStateContext.Provider>
  );
};

// Hook for using app state
export const useAppState = () => {
  const store = useContext(AppStateContext);
  if (!store) {
    throw new Error('useAppState must be used within AppStateProvider');
  }
  return store();
};

// Selector hooks for performance
export const useUser = () => useAppState().user;
export const useIsAuthenticated = () => useAppState().isAuthenticated;
export const useAIState = () => useAppState().ai;
export const useUIState = () => useAppState().ui;
export const useCurrentConversation = () => {
  const { ai } = useAppState();
  return ai.currentConversation ? ai.conversations[ai.currentConversation] : undefined;
};
export const useNotifications = () => useAppState().ui.notifications;
export const useUnreadNotificationCount = () => {
  const notifications = useNotifications();
  return notifications.filter(n => !n.read).length;
};
```

### 5.4 AI Integration Provider
```typescript
// src/providers/ai-provider.tsx
import React, { createContext, useContext, useEffect, useRef, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppState } from '../store/app-state';
import { coreConfig } from '../config/core.config';

interface AIProviderContext {
  socket: Socket | null;
  sendMessage: (conversationId: string, content: string) => Promise<void>;
  createConversation: (title: string, agentId?: string) => Promise<string>;
  executeTask: (type: string, parameters: any) => Promise<string>;
  getAgents: () => Promise<void>;
}

const AIContext = createContext<AIProviderContext | null>(null);

interface AIProviderProps {
  children: ReactNode;
}

export const AIProvider: React.FC<AIProviderProps> = ({ children }) => {
  const socketRef = useRef<Socket | null>(null);
  const {
    setAIConnection,
    addConversation,
    addMessage,
    updateAgent,
    addTask,
    updateTask,
    addNotification,
  } = useAppState();

  // Initialize WebSocket connection
  useEffect(() => {
    const socket = io(coreConfig.ai.websocket, {
      auth: {
        token: coreConfig.ai.apiKey,
      },
      timeout: coreConfig.ai.timeout,
      retries: coreConfig.ai.retryAttempts,
    });

    socketRef.current = socket;

    // Connection event handlers
    socket.on('connect', () => {
      console.log('Connected to AI service');
      setAIConnection(true);
      addNotification({
        type: 'success',
        title: 'AI Connected',
        message: 'Successfully connected to AI service',
      });
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from AI service');
      setAIConnection(false);
      addNotification({
        type: 'warning',
        title: 'AI Disconnected',
        message: 'Lost connection to AI service',
      });
    });

    socket.on('connect_error', (error) => {
      console.error('AI connection error:', error);
      setAIConnection(false);
      addNotification({
        type: 'error',
        title: 'AI Connection Error',
        message: 'Failed to connect to AI service',
      });
    });

    // Message event handlers
    socket.on('message', (data) => {
      const { conversationId, message } = data;
      addMessage(conversationId, {
        id: `msg-${Date.now()}-${Math.random()}`,
        content: message.content,
        role: message.role,
        timestamp: new Date(message.timestamp),
        metadata: message.metadata,
      });
    });

    // Agent event handlers
    socket.on('agent_status', (data) => {
      const { agentId, status } = data;
      updateAgent(agentId, { status });
    });

    socket.on('agents_list', (agents) => {
      agents.forEach((agent: any) => {
        updateAgent(agent.id, agent);
      });
    });

    // Task event handlers
    socket.on('task_created', (task) => {
      addTask({
        ...task,
        createdAt: new Date(task.createdAt),
        updatedAt: new Date(task.updatedAt),
      });
    });

    socket.on('task_updated', (data) => {
      const { taskId, updates } = data;
      updateTask(taskId, {
        ...updates,
        updatedAt: new Date(),
      });
    });

    socket.on('task_completed', (data) => {
      const { taskId, result } = data;
      updateTask(taskId, {
        status: 'completed',
        progress: 100,
        result,
        updatedAt: new Date(),
      });
      
      addNotification({
        type: 'success',
        title: 'Task Completed',
        message: `Task ${taskId} has been completed successfully`,
      });
    });

    socket.on('task_failed', (data) => {
      const { taskId, error } = data;
      updateTask(taskId, {
        status: 'failed',
        error,
        updatedAt: new Date(),
      });
      
      addNotification({
        type: 'error',
        title: 'Task Failed',
        message: `Task ${taskId} failed: ${error}`,
      });
    });

    // Request initial data
    socket.emit('get_agents');

    return () => {
      socket.disconnect();
    };
  }, []);

  // AI interaction methods
  const sendMessage = async (conversationId: string, content: string): Promise<void> => {
    if (!socketRef.current?.connected) {
      throw new Error('Not connected to AI service');
    }

    const message = {
      id: `msg-${Date.now()}-${Math.random()}`,
      content,
      role: 'user' as const,
      timestamp: new Date(),
    };

    // Add user message immediately
    addMessage(conversationId, message);

    // Send to AI service
    socketRef.current.emit('send_message', {
      conversationId,
      message,
    });
  };

  const createConversation = async (title: string, agentId?: string): Promise<string> => {
    if (!socketRef.current?.connected) {
      throw new Error('Not connected to AI service');
    }

    const conversationId = `conv-${Date.now()}-${Math.random()}`;
    const conversation = {
      id: conversationId,
      title,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      agentId,
    };

    addConversation(conversation);

    socketRef.current.emit('create_conversation', {
      conversationId,
      title,
      agentId,
    });

    return conversationId;
  };

  const executeTask = async (type: string, parameters: any): Promise<string> => {
    if (!socketRef.current?.connected) {
      throw new Error('Not connected to AI service');
    }

    const taskId = `task-${Date.now()}-${Math.random()}`;
    
    socketRef.current.emit('execute_task', {
      taskId,
      type,
      parameters,
    });

    return taskId;
  };

  const getAgents = async (): Promise<void> => {
    if (!socketRef.current?.connected) {
      throw new Error('Not connected to AI service');
    }

    socketRef.current.emit('get_agents');
  };

  const contextValue: AIProviderContext = {
    socket: socketRef.current,
    sendMessage,
    createConversation,
    executeTask,
    getAgents,
  };

  return (
    <AIContext.Provider value={contextValue}>
      {children}
    </AIContext.Provider>
  );
};

export const useAI = (): AIProviderContext => {
  const context = useContext(AIContext);
  if (!context) {
    throw new Error('useAI must be used within AIProvider');
  }
  return context;
};
```

### 5.5 Core Component Library
```typescript
// src/components/ui/button.tsx
import React, { forwardRef, ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../utils/cn';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

```typescript
// src/components/ai/chat-interface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { Button } from '../ui/button';
import { useAI } from '../../providers/ai-provider';
import { useCurrentConversation, useAppState } from '../../store/app-state';
import { cn } from '../../utils/cn';

interface ChatInterfaceProps {
  className?: string;
  conversationId?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  className,
  conversationId,
}) => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  
  const { sendMessage } = useAI();
  const conversation = useCurrentConversation();
  const { ai } = useAppState();
  
  const currentConversationId = conversationId || ai.currentConversation;
  const messages = currentConversationId ? ai.conversations[currentConversationId]?.messages || [] : [];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    if (!input.trim() || !currentConversationId || isLoading) return;

    const messageContent = input.trim();
    setInput('');
    setIsLoading(true);

    try {
      await sendMessage(currentConversationId, messageContent);
    } catch (error) {
      console.error('Failed to send message:', error);
      // TODO: Show error notification
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={cn('flex flex-col h-full', className)}>
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <div className="text-center">
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Start a conversation with the AI assistant</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                'flex items-start space-x-3',
                message.role === 'user' ? 'justify-end' : 'justify-start'
              )}
            >
              {message.role === 'assistant' && (
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-primary" />
                  </div>
                </div>
              )}
              
              <div
                className={cn(
                  'max-w-[70%] rounded-lg px-4 py-2',
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                )}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
              
              {message.role === 'user' && (
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                    <User className="w-4 h-4" />
                  </div>
                </div>
              )}
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Bot className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="bg-muted rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm text-muted-foreground">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="flex-1 resize-none border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 min-h-[40px] max-h-[120px]"
            rows={1}
            disabled={!currentConversationId || isLoading}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || !currentConversationId || isLoading}
            size="icon"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};
```

## 6. Common Pitfalls & Error Handling

### 6.1 State Management Issues
- **Problem**: State mutations causing re-render loops
- **Solution**: Use Immer middleware for immutable updates
- **Prevention**: Implement proper state selectors and memoization

### 6.2 WebSocket Connection Management
- **Problem**: Connection drops and reconnection failures
- **Solution**: Implement exponential backoff and connection health monitoring
- **Prevention**: Use connection pooling and heartbeat mechanisms

### 6.3 Component Performance
- **Problem**: Unnecessary re-renders and memory leaks
- **Solution**: Use React.memo, useMemo, and useCallback appropriately
- **Prevention**: Implement proper cleanup in useEffect hooks

### 6.4 Type Safety Issues
- **Problem**: Runtime type errors and API mismatches
- **Solution**: Use strict TypeScript configuration and runtime validation
- **Prevention**: Implement comprehensive type definitions and validation schemas

## 7. Performance Optimization

### 7.1 Bundle Optimization
- Implement code splitting and lazy loading
- Use tree shaking and dead code elimination
- Optimize asset loading and caching strategies

### 7.2 Runtime Performance
- Implement virtual scrolling for large lists
- Use Web Workers for heavy computations
- Optimize state updates and component rendering

### 7.3 Network Optimization
- Implement request deduplication and caching
- Use compression and efficient serialization
- Optimize WebSocket message handling

## 8. Integration with Genesis Engine

### 8.1 Agent Communication
- Integrate with Genesis agent protocols
- Implement cross-framework message routing
- Create unified agent management interface

### 8.2 State Synchronization
- Sync with Genesis state management
- Implement conflict resolution strategies
- Create real-time collaboration features

### 8.3 Development Workflow
- Integrate with Genesis development tools
- Implement hot reloading and live updates
- Create unified debugging and monitoring

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Set up component library and AI integration layer*