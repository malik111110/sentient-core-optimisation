-- Enable extensions required by Supabase and for vector operations
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";
create extension if not exists "pgvector";

-- Main table to track the state of entire agentic workflows
create table if not exists workflow_states (
  id uuid primary key default uuid_generate_v4(),
  project_name text not null,
  status text not null check (status in ('running', 'completed', 'failed')),
  tasks jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
comment on table workflow_states is 'Tracks high-level state for a multi-agent workflow.';

-- Event log for all actions taken by agents
create table if not exists agent_events (
  id uuid primary key default uuid_generate_v4(),
  event_type text not null,
  source_agent text not null,
  workflow_id uuid references workflow_states(id) on delete cascade,
  task_id text,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
comment on table agent_events is 'Logs every event emitted by agents for debugging and replay.';

-- Table for storing vector embeddings for semantic search
create table if not exists document_embeddings (
  id uuid primary key default uuid_generate_v4(),
  content text not null,
  embedding vector(1536),  -- Dimension for OpenAI text-embedding-ada-002
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
comment on table document_embeddings is 'Stores vector embeddings of documents for semantic search.';

-- Indexes for performance
create index if not exists idx_workflow_status on workflow_states(status);
create index if not exists idx_events_workflow on agent_events(workflow_id);
-- Using HNSW index for pgvector >= 0.5.0, which is standard in recent Supabase images
create index if not exists idx_embeddings_vector on document_embeddings using hnsw (embedding vector_cosine_ops);
