-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create document_embeddings table with vector type
CREATE TABLE IF NOT EXISTS public.document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),  -- For OpenAI's text-embedding-ada-002
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create HNSW index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
ON public.document_embeddings 
USING hnsw (embedding vector_cosine_ops);

-- Verify the extension and table were created
SELECT '✅ pgvector extension installed' as status
WHERE EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector');

SELECT '✅ document_embeddings table exists' as status
WHERE EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'document_embeddings'
);
