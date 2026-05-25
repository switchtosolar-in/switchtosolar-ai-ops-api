BEGIN;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS request_id TEXT;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS retrieved_chunk_ids TEXT;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS similarity_scores TEXT;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS model_used TEXT;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS status TEXT;
ALTER TABLE query_logs
ADD COLUMN IF NOT EXISTS error_message TEXT;
CREATE INDEX IF NOT EXISTS idx_query_logs_request_id ON query_logs (request_id);
INSERT INTO schema_migrations (migration_name)
VALUES ('2026_04_06_002_expand_query_logs.sql') ON CONFLICT (migration_name) DO NOTHING;
COMMIT;