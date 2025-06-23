-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS "pgvector" WITH SCHEMA public;

-- Create workflow_states table
CREATE TABLE IF NOT EXISTS public.workflow_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    tasks JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create agent_events table
CREATE TABLE IF NOT EXISTS public.agent_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type TEXT NOT NULL,
    source_agent TEXT NOT NULL,
    workflow_id UUID REFERENCES public.workflow_states(id) ON DELETE CASCADE,
    task_id TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create document_embeddings table
CREATE TABLE IF NOT EXISTS public.document_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),  -- For OpenAI's text-embedding-ada-002
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_workflow_status ON public.workflow_states(status);
CREATE INDEX IF NOT EXISTS idx_events_workflow ON public.agent_events(workflow_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON public.document_embeddings USING hnsw (embedding vector_cosine_ops);

-- Verify the setup
SELECT '✅ Database setup complete' as status;
