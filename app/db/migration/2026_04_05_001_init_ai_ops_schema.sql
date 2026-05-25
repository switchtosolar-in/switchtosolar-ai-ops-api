BEGIN;
-- Step 1: Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
-- Step 2: Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    source_path TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
-- Step 3: Create document_chunks table
CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    chunk_index INTEGER,
    chunk_text TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);
-- Step 4: Create query_logs table
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    question TEXT,
    answer TEXT,
    intent_type TEXT,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
-- Step 5: Create schema_migrations table (if not exists)
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    migration_name TEXT UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT NOW()
);
-- Step 6: Log this migration (safe insert)
INSERT INTO schema_migrations (migration_name)
VALUES ('2026_04_05_001_init_ai_ops_schema.sql') ON CONFLICT (migration_name) DO NOTHING;
COMMIT;
###docker exec -i switchtosolar-ai-postgres psql -U s2s_ai_user -d switchtosolar_ai_ops < app/db/migrations/2026_05_05_001_init_ai_ops_schema.sql