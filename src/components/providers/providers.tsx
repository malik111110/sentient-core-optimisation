'use client'

import { ReactNode, createContext, useContext, useEffect, useState } from 'react'
import { wsClient } from '@/lib/websocket'
import { Agent, Task, Project } from '@/types'

// Theme Provider Context
interface ThemeContextType {
  theme: 'light' | 'dark' | 'system'
  setTheme: (theme: 'light' | 'dark' | 'system') => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

// WebSocket Provider Context
interface WebSocketContextType {
  ws: typeof wsClient | null
  isConnected: boolean
  agents: Agent[]
  tasks: Task[]
  projects: Project[]
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined)

export const useWebSocket = () => {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider')
  }
  return context
}

// Theme Provider Component
interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: 'light' | 'dark' | 'system'
}

export function ThemeProvider({ children, defaultTheme = 'system' }: ThemeProviderProps) {
  const [theme, setTheme] = useState<'light' | 'dark' | 'system'>(defaultTheme)

  useEffect(() => {
    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | 'system' | null
    if (savedTheme) {
      setTheme(savedTheme)
    }
  }, [])

  useEffect(() => {
    // Apply theme to document
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      root.classList.add(systemTheme)
    } else {
      root.classList.add(theme)
    }

    // Save to localStorage
    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// WebSocket Provider Component
interface WebSocketProviderProps {
  children: ReactNode
}

export function WebSocketProvider({ children }: WebSocketProviderProps) {
  const [ws, setWs] = useState<typeof wsClient | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [agents, setAgents] = useState<Agent[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    // Initialize WebSocket connection
    setWs(wsClient)

    // Set up event listeners
    wsClient.on('connect', () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    })

    wsClient.on('disconnect', () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')
    })

    wsClient.on('agent_status', (data: { agents: Agent[] }) => {
      setAgents(data.agents)
    })

    wsClient.on('task_update', (data: { tasks: Task[] }) => {
      setTasks(data.tasks)
    })

    wsClient.on('project_update', (data: { projects: Project[] }) => {
      setProjects(data.projects)
    })

    // Connect
    wsClient.connect()

    // Cleanup on unmount
    return () => {
      wsClient.disconnect()
    }
  }, [])

  return (
    <WebSocketContext.Provider value={{ ws, isConnected, agents, tasks, projects }}>
      {children}
    </WebSocketContext.Provider>
  )
}

// Combined Providers Component
interface ProvidersProps {
  children: ReactNode
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider>
      <WebSocketProvider>
        {children}
      </WebSocketProvider>
    </ThemeProvider>
  )
}