-- Database schema for PostgreSQL (Aurora/RDS)
-- Logs resume optimization requests and prompt edits

-- Table: optimization_logs
-- Logs every resume optimization request
CREATE TABLE IF NOT EXISTS optimization_logs (
  id BIGSERIAL PRIMARY KEY,
  resume_text TEXT,
  job_description TEXT,
  custom_prompt TEXT,
  response_data JSONB,
  duration_ms INTEGER,
  status_code INTEGER,
  error_message TEXT,
  user_ip VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_optimization_logs_created_at ON optimization_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_optimization_logs_status_code ON optimization_logs(status_code);

-- Table: prompt_edits
-- Logs when users customize the prompt
CREATE TABLE IF NOT EXISTS prompt_edits (
  id BIGSERIAL PRIMARY KEY,
  original_prompt TEXT,
  edited_prompt TEXT,
  user_ip VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_prompt_edits_created_at ON prompt_edits(created_at);

-- Optional: Table for analytics/summary
CREATE TABLE IF NOT EXISTS request_summary (
  id BIGSERIAL PRIMARY KEY,
  date DATE UNIQUE,
  total_requests INTEGER DEFAULT 0,
  successful_requests INTEGER DEFAULT 0,
  failed_requests INTEGER DEFAULT 0,
  avg_duration_ms DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_request_summary_updated_at 
  BEFORE UPDATE ON request_summary
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
