/**
 * Genesis Engine Core Types
 * TypeScript definitions for the Genesis Agentic Development Engine
 */

// Agent Types
export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  status: AgentStatus;
  capabilities: string[];
  currentTask?: Task;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export type AgentType = 
  | 'AGENT-REQUIREMENTS'
  | 'AGENT-ARCHITECT'
  | 'AGENT-FRONTEND'
  | 'AGENT-BACKEND'
  | 'AGENT-DATABASE'
  | 'AGENT-DEVOPS'
  | 'AGENT-QA'
  | 'AGENT-SECURITY'
  | 'AGENT-DOCS';

export type AgentStatus = 
  | 'idle'
  | 'working'
  | 'waiting'
  | 'error'
  | 'offline';

// Task Types
export interface Task {
  id: string;
  title: string;
  description: string;
  type: TaskType;
  priority: TaskPriority;
  status: TaskStatus;
  assignedAgent?: string;
  dependencies: string[];
  estimatedDuration: number;
  actualDuration?: number;
  progress: number;
  artifacts: Artifact[];
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
}

export type TaskType = 
  | 'epic'
  | 'story'
  | 'task'
  | 'subtask'
  | 'bug'
  | 'enhancement';

export type TaskPriority = 
  | 'P0' // Critical
  | 'P1' // High
  | 'P2' // Medium
  | 'P3'; // Low

export type TaskStatus = 
  | 'backlog'
  | 'todo'
  | 'in_progress'
  | 'review'
  | 'testing'
  | 'done'
  | 'blocked';

// Artifact Types
export interface Artifact {
  id: string;
  name: string;
  type: ArtifactType;
  content: string;
  language?: string;
  path?: string;
  size: number;
  checksum: string;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export type ArtifactType = 
  | 'code'
  | 'documentation'
  | 'configuration'
  | 'test'
  | 'schema'
  | 'asset'
  | 'template';

// Project Types
export interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  techStack: TechStack;
  agents: Agent[];
  tasks: Task[];
  artifacts: Artifact[];
  settings: ProjectSettings;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export type ProjectStatus = 
  | 'planning'
  | 'development'
  | 'testing'
  | 'deployment'
  | 'completed'
  | 'paused'
  | 'cancelled';

export interface TechStack {
  frontend: string[];
  backend: string[];
  database: string[];
  infrastructure: string[];
  tools: string[];
}

export interface ProjectSettings {
  enableRealTimeUpdates: boolean;
  enableAutoSave: boolean;
  enableCollaboration: boolean;
  codeStyle: CodeStyleSettings;
  deployment: DeploymentSettings;
}

export interface CodeStyleSettings {
  formatter: 'prettier' | 'eslint';
  tabSize: number;
  useTabs: boolean;
  semicolons: boolean;
  quotes: 'single' | 'double';
  trailingCommas: boolean;
}

export interface DeploymentSettings {
  provider: 'vercel' | 'netlify' | 'aws' | 'gcp' | 'azure';
  environment: 'development' | 'staging' | 'production';
  autoDeployment: boolean;
  customDomain?: string;
}

// Communication Types
export interface Message {
  id: string;
  type: MessageType;
  sender: string;
  recipient?: string;
  content: any;
  timestamp: Date;
  metadata: Record<string, any>;
}

export type MessageType = 
  | 'task_assignment'
  | 'task_update'
  | 'task_completion'
  | 'agent_status'
  | 'error'
  | 'notification'
  | 'collaboration';

// UI Types
export interface UIState {
  theme: 'light' | 'dark' | 'system';
  sidebarCollapsed: boolean;
  activePanel: string;
  openTabs: Tab[];
  notifications: Notification[];
}

export interface Tab {
  id: string;
  title: string;
  type: 'code' | 'preview' | 'terminal' | 'documentation';
  content?: string;
  path?: string;
  isDirty: boolean;
}

export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  actions?: NotificationAction[];
}

export interface NotificationAction {
  label: string;
  action: () => void;
  variant?: 'primary' | 'secondary' | 'destructive';
}

// API Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: Date;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// WebSocket Types
export interface WebSocketMessage {
  type: string;
  payload: any;
  timestamp: Date;
}

export interface WebSocketState {
  connected: boolean;
  reconnecting: boolean;
  lastConnected?: Date;
  lastDisconnected?: Date;
  reconnectAttempts: number;
}