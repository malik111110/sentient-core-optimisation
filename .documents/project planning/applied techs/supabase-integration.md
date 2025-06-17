# Supabase Integration Guide

**ID:** guide:feature:supabase_integration  
**Source Reference(s):** /database/supabase  
**Last Validated:** June 2025

## 1. Purpose

Implement comprehensive Supabase integration for the Genesis Engine, providing authentication, real-time database operations, file storage, and edge functions for a complete backend-as-a-service solution.

## 2. Key Concepts

- **PostgreSQL Database**: Fully managed PostgreSQL with real-time subscriptions
- **Authentication**: Built-in auth with multiple providers and row-level security
- **Real-time Subscriptions**: Live data updates using WebSocket connections
- **Storage**: File upload and management with CDN integration
- **Edge Functions**: Serverless functions for custom backend logic
- **Row Level Security (RLS)**: Database-level security policies
- **API Auto-generation**: Automatic REST and GraphQL APIs

## 3. Required Dependencies

### Frontend Dependencies
```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.43.4",
    "@supabase/ssr": "^0.3.0",
    "@supabase/auth-ui-react": "^0.4.7",
    "@supabase/auth-ui-shared": "^0.1.8"
  }
}
```

### Python Dependencies
```python
# requirements.txt
supabase==2.3.0
postgrest-py==0.13.0
realtime-py==0.1.0
storage3==0.7.0
gotrue==2.3.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
alembic==1.13.1
pydantic==2.5.0
```

### Environment Variables
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Database Configuration
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
DIRECT_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres

# Storage Configuration
SUPABASE_STORAGE_BUCKET=genesis-files
SUPABASE_STORAGE_URL=https://your-project.supabase.co/storage/v1

# Auth Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## 4. Step-by-Step Implementation Plan

### 4.1 Project Setup and Configuration
1. Create Supabase project and obtain credentials
2. Set up local development environment
3. Configure environment variables
4. Initialize Supabase client
5. Set up database migrations

### 4.2 Database Schema Design
1. Design core tables for Genesis Engine
2. Implement Row Level Security policies
3. Create database functions and triggers
4. Set up real-time subscriptions
5. Configure indexes and performance optimization

### 4.3 Authentication Implementation
1. Set up authentication providers
2. Implement user registration and login
3. Configure session management
4. Set up role-based access control
5. Implement password reset and email verification

### 4.4 Real-time Features
1. Set up real-time subscriptions
2. Implement live data synchronization
3. Create collaborative features
4. Handle connection management
5. Implement conflict resolution

### 4.5 File Storage Integration
1. Configure storage buckets
2. Implement file upload/download
3. Set up image optimization
4. Create file sharing mechanisms
5. Implement storage policies

## 5. Core Code Example

### 5.1 Supabase Client Configuration for Next.js (App Router)

This section outlines how to set up Supabase client instances for different Next.js contexts using the `@supabase/ssr` package, which is designed for server-side rendering and auth management in Next.js.

#### 5.1.1 Client-Side Component Utility (`lib/supabase/client.ts`)

This utility creates a Supabase client instance for use in Client Components.

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';
import type { Database } from './database.types'; // Assuming you have generated types

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

**Usage in a Client Component:**
```typescript
// app/some-client-component.tsx
'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client'; // Adjust path as needed
import type { User } from '@supabase/supabase-js';

export default function SomeClientComponent() {
  const supabase = createClient();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);

  async update<T>(table: string, id: string, data: Partial<T>) {
    const { data: result, error } = await this.client
      .from(table)
      .update(data)
      .eq('id', id)
      .select()
      .single();

    if (error) throw new Error(error.message);
    return result as T;
  }

  async delete(table: string, id: string) {
    const { error } = await this.client
      .from(table)
      .delete()
      .eq('id', id);

    if (error) throw new Error(error.message);
  }

  // Real-time subscriptions
  subscribe<T>(
    table: string,
    callback: (payload: any) => void,
    filter?: string
  ) {
    const channel = this.client
      .channel(`${table}-changes`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table,
          filter
        },
        callback
      )
      .subscribe();

    return () => {
      this.client.removeChannel(channel);
    };
  }

  // Storage methods
  async uploadFile(bucket: string, path: string, file: File) {
    const { data, error } = await this.client.storage
      .from(bucket)
      .upload(path, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (error) throw new Error(error.message);
    return data;
  }

  async downloadFile(bucket: string, path: string) {
    const { data, error } = await this.client.storage
      .from(bucket)
      .download(path);

    if (error) throw new Error(error.message);
    return data;
  }

  getPublicUrl(bucket: string, path: string) {
    const { data } = this.client.storage
      .from(bucket)
      .getPublicUrl(path);

    return data.publicUrl;
  }
}

export const supabaseService = new SupabaseService();
```

### 5.2 Database Schema Definition
```sql
-- Database schema for Genesis Engine
-- File: supabase/migrations/001_initial_schema.sql

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (extends auth.users)
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'developer')),
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects table
CREATE TABLE public.projects (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  settings JSONB DEFAULT '{}',
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project collaborators
CREATE TABLE public.project_collaborators (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'viewer' CHECK (role IN ('owner', 'editor', 'viewer')),
  permissions JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(project_id, user_id)
);

-- Agents table
CREATE TABLE public.agents (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('architect', 'frontend', 'backend', 'tester', 'debugger')),
  description TEXT,
  configuration JSONB DEFAULT '{}',
  system_prompt TEXT,
  model_provider TEXT DEFAULT 'openai',
  model_name TEXT DEFAULT 'gpt-4',
  tools JSONB DEFAULT '[]',
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
  created_by UUID REFERENCES public.profiles(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workflows table
CREATE TABLE public.workflows (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  definition JSONB NOT NULL, -- LangGraph workflow definition
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'completed', 'failed')),
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_by UUID REFERENCES public.profiles(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workflow executions
CREATE TABLE public.workflow_executions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE,
  state JSONB NOT NULL, -- Current workflow state
  status TEXT DEFAULT 'running' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
  error_message TEXT,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent tasks
CREATE TABLE public.agent_tasks (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  workflow_execution_id UUID REFERENCES public.workflow_executions(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES public.agents(id),
  agent_type TEXT NOT NULL,
  input_data JSONB,
  output_data JSONB,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
  error_message TEXT,
  execution_time_ms INTEGER,
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Code artifacts
CREATE TABLE public.code_artifacts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  task_id UUID REFERENCES public.agent_tasks(id),
  name TEXT NOT NULL,
  file_path TEXT,
  language TEXT,
  content TEXT NOT NULL,
  type TEXT DEFAULT 'file' CHECK (type IN ('file', 'component', 'snippet')),
  version INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}',
  created_by UUID REFERENCES public.profiles(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat sessions
CREATE TABLE public.chat_sessions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  title TEXT,
  context JSONB DEFAULT '{}',
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat messages
CREATE TABLE public.chat_messages (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  session_id UUID REFERENCES public.chat_sessions(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  artifacts JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- File storage metadata
CREATE TABLE public.file_storage (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  bucket_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_size BIGINT,
  mime_type TEXT,
  public_url TEXT,
  metadata JSONB DEFAULT '{}',
  uploaded_by UUID REFERENCES public.profiles(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(bucket_name, file_path)
);

-- Create indexes for performance
CREATE INDEX idx_projects_owner_id ON public.projects(owner_id);
CREATE INDEX idx_project_collaborators_project_id ON public.project_collaborators(project_id);
CREATE INDEX idx_project_collaborators_user_id ON public.project_collaborators(user_id);
CREATE INDEX idx_workflows_project_id ON public.workflows(project_id);
CREATE INDEX idx_workflow_executions_workflow_id ON public.workflow_executions(workflow_id);
CREATE INDEX idx_agent_tasks_workflow_execution_id ON public.agent_tasks(workflow_execution_id);
CREATE INDEX idx_agent_tasks_agent_id ON public.agent_tasks(agent_id);
CREATE INDEX idx_code_artifacts_project_id ON public.code_artifacts(project_id);
CREATE INDEX idx_code_artifacts_task_id ON public.code_artifacts(task_id);
CREATE INDEX idx_chat_sessions_project_id ON public.chat_sessions(project_id);
CREATE INDEX idx_chat_sessions_user_id ON public.chat_sessions(user_id);
CREATE INDEX idx_chat_messages_session_id ON public.chat_messages(session_id);
CREATE INDEX idx_file_storage_project_id ON public.file_storage(project_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON public.projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON public.agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON public.workflows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_code_artifacts_updated_at BEFORE UPDATE ON public.code_artifacts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON public.chat_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 5.3 Row Level Security Policies
```sql
-- RLS policies for Genesis Engine
-- File: supabase/migrations/002_rls_policies.sql

-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.project_collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflow_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.code_artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.file_storage ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view their own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON public.profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Projects policies
CREATE POLICY "Users can view projects they own or collaborate on" ON public.projects
  FOR SELECT USING (
    owner_id = auth.uid() OR
    id IN (
      SELECT project_id FROM public.project_collaborators
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Users can create projects" ON public.projects
  FOR INSERT WITH CHECK (owner_id = auth.uid());

CREATE POLICY "Project owners can update their projects" ON public.projects
  FOR UPDATE USING (owner_id = auth.uid());

CREATE POLICY "Project owners can delete their projects" ON public.projects
  FOR DELETE USING (owner_id = auth.uid());

-- Project collaborators policies
CREATE POLICY "Users can view collaborators of their projects" ON public.project_collaborators
  FOR SELECT USING (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Project owners can manage collaborators" ON public.project_collaborators
  FOR ALL USING (
    project_id IN (
      SELECT id FROM public.projects WHERE owner_id = auth.uid()
    )
  );

-- Workflows policies
CREATE POLICY "Users can view workflows of their projects" ON public.workflows
  FOR SELECT USING (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Users can create workflows in their projects" ON public.workflows
  FOR INSERT WITH CHECK (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid() AND role IN ('owner', 'editor')
      )
    ) AND created_by = auth.uid()
  );

-- Chat sessions policies
CREATE POLICY "Users can view their own chat sessions" ON public.chat_sessions
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create chat sessions" ON public.chat_sessions
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own chat sessions" ON public.chat_sessions
  FOR UPDATE USING (user_id = auth.uid());

-- Chat messages policies
CREATE POLICY "Users can view messages from their sessions" ON public.chat_messages
  FOR SELECT USING (
    session_id IN (
      SELECT id FROM public.chat_sessions WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert messages to their sessions" ON public.chat_messages
  FOR INSERT WITH CHECK (
    session_id IN (
      SELECT id FROM public.chat_sessions WHERE user_id = auth.uid()
    )
  );

-- Code artifacts policies
CREATE POLICY "Users can view artifacts from their projects" ON public.code_artifacts
  FOR SELECT USING (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Users can create artifacts in their projects" ON public.code_artifacts
  FOR INSERT WITH CHECK (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid() AND role IN ('owner', 'editor')
      )
    ) AND created_by = auth.uid()
  );

-- File storage policies
CREATE POLICY "Users can view files from their projects" ON public.file_storage
  FOR SELECT USING (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Users can upload files to their projects" ON public.file_storage
  FOR INSERT WITH CHECK (
    project_id IN (
      SELECT id FROM public.projects
      WHERE owner_id = auth.uid() OR
      id IN (
        SELECT project_id FROM public.project_collaborators
        WHERE user_id = auth.uid() AND role IN ('owner', 'editor')
      )
    ) AND uploaded_by = auth.uid()
  );
```

### 5.4 Real-time Hooks Implementation
```typescript
// hooks/useRealtimeSubscription.ts
import { useEffect, useState, useCallback } from 'react';
import { supabase } from '~/lib/supabase/client';
import type { RealtimeChannel } from '@supabase/supabase-js';

export interface RealtimeSubscriptionOptions {
  table: string;
  filter?: string;
  event?: 'INSERT' | 'UPDATE' | 'DELETE' | '*';
  schema?: string;
}

export function useRealtimeSubscription<T>(
  options: RealtimeSubscriptionOptions,
  onData: (payload: any) => void,
  dependencies: any[] = []
) {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [channel, setChannel] = useState<RealtimeChannel | null>(null);

  const subscribe = useCallback(() => {
    const channelName = `${options.table}-${Date.now()}`;
    
    const newChannel = supabase
      .channel(channelName)
      .on(
        'postgres_changes',
        {
          event: options.event || '*',
          schema: options.schema || 'public',
          table: options.table,
          filter: options.filter
        },
        (payload) => {
          console.log('Realtime payload:', payload);
          onData(payload);
        }
      )
      .subscribe((status) => {
        console.log('Subscription status:', status);
        setIsConnected(status === 'SUBSCRIBED');
        
        if (status === 'CHANNEL_ERROR') {
          setError('Failed to subscribe to realtime updates');
        } else {
          setError(null);
        }
      });

    setChannel(newChannel);
    return newChannel;
  }, [options.table, options.filter, options.event, options.schema, onData]);

  const unsubscribe = useCallback(() => {
    if (channel) {
      supabase.removeChannel(channel);
      setChannel(null);
      setIsConnected(false);
    }
  }, [channel]);

  useEffect(() => {
    const newChannel = subscribe();
    
    return () => {
      supabase.removeChannel(newChannel);
    };
  }, dependencies);

  return {
    isConnected,
    error,
    subscribe,
    unsubscribe
  };
}

// hooks/useProject.ts
import { useState, useEffect } from 'react';
import { supabaseService } from '~/lib/supabase/client';
import { useRealtimeSubscription } from './useRealtimeSubscription';

export interface Project {
  id: string;
  name: string;
  description?: string;
  owner_id: string;
  settings: Record<string, any>;
  status: 'active' | 'archived' | 'deleted';
  created_at: string;
  updated_at: string;
}

export function useProject(projectId: string) {
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load initial project data
  useEffect(() => {
    async function loadProject() {
      try {
        setLoading(true);
        const { data, error } = await supabaseService.client
          .from('projects')
          .select('*')
          .eq('id', projectId)
          .single();

        if (error) throw error;
        setProject(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load project');
      } finally {
        setLoading(false);
      }
    }

    if (projectId) {
      loadProject();
    }
  }, [projectId]);

  // Subscribe to real-time updates
  useRealtimeSubscription(
    {
      table: 'projects',
      filter: `id=eq.${projectId}`
    },
    (payload) => {
      if (payload.eventType === 'UPDATE' && payload.new) {
        setProject(payload.new as Project);
      } else if (payload.eventType === 'DELETE') {
        setProject(null);
      }
    },
    [projectId]
  );

  const updateProject = async (updates: Partial<Project>) => {
    try {
      const updatedProject = await supabaseService.update('projects', projectId, updates);
      setProject(updatedProject);
      return updatedProject;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update project');
      throw err;
    }
  };

  return {
    project,
    loading,
    error,
    updateProject
  };
}

// hooks/useChatSession.ts
import { useState, useEffect, useCallback } from 'react';
import { supabaseService } from '~/lib/supabase/client';
import { useRealtimeSubscription } from './useRealtimeSubscription';

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  artifacts: any[];
  metadata: Record<string, any>;
  created_at: string;
}

export interface ChatSession {
  id: string;
  project_id: string;
  user_id: string;
  title?: string;
  context: Record<string, any>;
  status: 'active' | 'archived';
  created_at: string;
  updated_at: string;
}

export function useChatSession(sessionId: string) {
  const [session, setSession] = useState<ChatSession | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load session and messages
  useEffect(() => {
    async function loadSessionData() {
      try {
        setLoading(true);
        
        // Load session
        const { data: sessionData, error: sessionError } = await supabaseService.client
          .from('chat_sessions')
          .select('*')
          .eq('id', sessionId)
          .single();

        if (sessionError) throw sessionError;
        setSession(sessionData);

        // Load messages
        const { data: messagesData, error: messagesError } = await supabaseService.client
          .from('chat_messages')
          .select('*')
          .eq('session_id', sessionId)
          .order('created_at', { ascending: true });

        if (messagesError) throw messagesError;
        setMessages(messagesData || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load chat session');
      } finally {
        setLoading(false);
      }
    }

    if (sessionId) {
      loadSessionData();
    }
  }, [sessionId]);

  // Subscribe to new messages
  useRealtimeSubscription(
    {
      table: 'chat_messages',
      filter: `session_id=eq.${sessionId}`,
      event: 'INSERT'
    },
    (payload) => {
      if (payload.new) {
        setMessages(prev => [...prev, payload.new as ChatMessage]);
      }
    },
    [sessionId]
  );

  const addMessage = useCallback(async (message: Omit<ChatMessage, 'id' | 'created_at'>) => {
    try {
      const newMessage = await supabaseService.insert('chat_messages', {
        ...message,
        session_id: sessionId
      });
      return newMessage;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add message');
      throw err;
    }
  }, [sessionId]);

  const updateSession = useCallback(async (updates: Partial<ChatSession>) => {
    try {
      const updatedSession = await supabaseService.update('chat_sessions', sessionId, updates);
      setSession(updatedSession);
      return updatedSession;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update session');
      throw err;
    }
  }, [sessionId]);

  return {
    session,
    messages,
    loading,
    error,
    addMessage,
    updateSession
  };
}
```

### 5.5 Python Integration
```python
# lib/supabase_client.py
import os
from typing import Dict, List, Optional, Any
from supabase import create_client, Client
from gotrue import User
import asyncio
from datetime import datetime
import json

class SupabaseClient:
    """Python client for Supabase integration"""
    
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        
        self.client: Client = create_client(url, key)
    
    # Authentication methods
    async def create_user(self, email: str, password: str, metadata: Dict[str, Any] = None) -> Dict:
        """Create a new user account"""
        try:
            response = self.client.auth.admin.create_user({
                "email": email,
                "password": password,
                "user_metadata": metadata or {},
                "email_confirm": True
            })
            return response.dict()
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = self.client.auth.admin.get_user_by_id(user_id)
            return response.dict() if response else None
        except Exception as e:
            print(f"Failed to get user: {str(e)}")
            return None
    
    # Database operations
    async def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record into a table"""
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            raise Exception(f"Failed to insert record: {str(e)}")
    
    async def update_record(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record in a table"""
        try:
            response = self.client.table(table).update(data).eq("id", record_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            raise Exception(f"Failed to update record: {str(e)}")
    
    async def get_record(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID"""
        try:
            response = self.client.table(table).select("*").eq("id", record_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Failed to get record: {str(e)}")
            return None
    
    async def query_records(
        self, 
        table: str, 
        filters: Dict[str, Any] = None,
        select: str = "*",
        order_by: str = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """Query records with filters"""
        try:
            query = self.client.table(table).select(select)
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            if order_by:
                query = query.order(order_by)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            print(f"Failed to query records: {str(e)}")
            return []
    
    async def delete_record(self, table: str, record_id: str) -> bool:
        """Delete a record by ID"""
        try:
            response = self.client.table(table).delete().eq("id", record_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Failed to delete record: {str(e)}")
            return False
    
    # Project-specific methods
    async def create_project(
        self, 
        name: str, 
        description: str, 
        owner_id: str,
        settings: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a new project"""
        project_data = {
            "name": name,
            "description": description,
            "owner_id": owner_id,
            "settings": settings or {},
            "status": "active"
        }
        return await self.insert_record("projects", project_data)
    
    async def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        # Get owned projects
        owned_projects = await self.query_records(
            "projects",
            filters={"owner_id": user_id, "status": "active"}
        )
        
        # Get collaborated projects
        collaborations = await self.query_records(
            "project_collaborators",
            filters={"user_id": user_id}
        )
        
        collaborated_project_ids = [c["project_id"] for c in collaborations]
        collaborated_projects = []
        
        for project_id in collaborated_project_ids:
            project = await self.get_record("projects", project_id)
            if project and project["status"] == "active":
                collaborated_projects.append(project)
        
        return owned_projects + collaborated_projects
    
    async def create_workflow(
        self,
        project_id: str,
        name: str,
        description: str,
        definition: Dict[str, Any],
        created_by: str
    ) -> Dict[str, Any]:
        """Create a new workflow"""
        workflow_data = {
            "project_id": project_id,
            "name": name,
            "description": description,
            "definition": definition,
            "status": "draft",
            "created_by": created_by
        }
        return await self.insert_record("workflows", workflow_data)
    
    async def start_workflow_execution(
        self,
        workflow_id: str,
        initial_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start a workflow execution"""
        execution_data = {
            "workflow_id": workflow_id,
            "state": initial_state,
            "status": "running",
            "started_at": datetime.now().isoformat()
        }
        return await self.insert_record("workflow_executions", execution_data)
    
    async def update_workflow_execution(
        self,
        execution_id: str,
        state: Dict[str, Any],
        status: str = None,
        error_message: str = None
    ) -> Dict[str, Any]:
        """Update workflow execution state"""
        update_data = {"state": state}
        
        if status:
            update_data["status"] = status
            
            if status in ["completed", "failed", "cancelled"]:
                update_data["completed_at"] = datetime.now().isoformat()
        
        if error_message:
            update_data["error_message"] = error_message
        
        return await self.update_record("workflow_executions", execution_id, update_data)
    
    async def create_agent_task(
        self,
        workflow_execution_id: str,
        agent_id: str,
        agent_type: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new agent task"""
        task_data = {
            "workflow_execution_id": workflow_execution_id,
            "agent_id": agent_id,
            "agent_type": agent_type,
            "input_data": input_data,
            "status": "pending"
        }
        return await self.insert_record("agent_tasks", task_data)
    
    async def complete_agent_task(
        self,
        task_id: str,
        output_data: Dict[str, Any],
        execution_time_ms: int,
        status: str = "completed",
        error_message: str = None
    ) -> Dict[str, Any]:
        """Complete an agent task"""
        update_data = {
            "output_data": output_data,
            "execution_time_ms": execution_time_ms,
            "status": status,
            "completed_at": datetime.now().isoformat()
        }
        
        if error_message:
            update_data["error_message"] = error_message
        
        return await self.update_record("agent_tasks", task_id, update_data)
    
    async def save_code_artifact(
        self,
        project_id: str,
        task_id: str,
        name: str,
        file_path: str,
        language: str,
        content: str,
        artifact_type: str = "file",
        created_by: str = None
    ) -> Dict[str, Any]:
        """Save a code artifact"""
        artifact_data = {
            "project_id": project_id,
            "task_id": task_id,
            "name": name,
            "file_path": file_path,
            "language": language,
            "content": content,
            "type": artifact_type,
            "version": 1,
            "is_active": True,
            "created_by": created_by
        }
        return await self.insert_record("code_artifacts", artifact_data)
    
    # Storage methods
    async def upload_file(
        self,
        bucket: str,
        file_path: str,
        file_data: bytes,
        content_type: str = None
    ) -> Dict[str, Any]:
        """Upload a file to storage"""
        try:
            response = self.client.storage.from_(bucket).upload(
                file_path,
                file_data,
                file_options={
                    "content-type": content_type,
                    "cache-control": "3600"
                }
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    async def get_file_url(self, bucket: str, file_path: str) -> str:
        """Get public URL for a file"""
        try:
            response = self.client.storage.from_(bucket).get_public_url(file_path)
            return response["publicURL"]
        except Exception as e:
            raise Exception(f"Failed to get file URL: {str(e)}")

# Global instance
supabase_client = SupabaseClient()
```

## 6. Common Pitfalls & Error Handling

### 6.1 Row Level Security Issues
- **Problem**: Users can't access data due to overly restrictive RLS policies
- **Solution**: Test policies thoroughly and implement proper role-based access
- **Prevention**: Use policy testing and implement gradual rollout

### 6.2 Real-time Connection Management
- **Problem**: Real-time subscriptions fail or consume too many connections
- **Solution**: Implement connection pooling and proper cleanup
- **Detection**: Monitor connection counts and implement heartbeat checks

### 6.3 Database Performance
- **Problem**: Slow queries due to missing indexes or inefficient queries
- **Solution**: Implement proper indexing and query optimization
- **Monitoring**: Use Supabase dashboard and query analysis tools

### 6.4 Authentication Edge Cases
- **Problem**: Session management issues and token expiration
- **Solution**: Implement proper token refresh and error handling
- **Prevention**: Use auth helpers and implement retry mechanisms

## 7. Performance Optimization

### 7.1 Database Optimization
- Implement proper indexing strategies
- Use database functions for complex operations
- Optimize query patterns and reduce N+1 queries

### 7.2 Real-time Optimization
- Limit subscription scope with filters
- Implement connection pooling
- Use batch updates for multiple changes

### 7.3 Storage Optimization
- Implement CDN caching
- Use image optimization and compression
- Implement lazy loading for large files

## 8. Integration with Genesis Engine

### 8.1 Multi-Agent Workflow Storage
- Store workflow definitions and execution state
- Track agent task progress and results
- Implement workflow versioning and rollback

### 8.2 Real-time Collaboration
- Live updates for multi-user projects
- Real-time chat and code sharing
- Collaborative editing with conflict resolution

### 8.3 Analytics and Monitoring
- Track user engagement and feature usage
- Monitor system performance and errors
- Implement usage analytics and reporting

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Set up production database and implement advanced real-time features*