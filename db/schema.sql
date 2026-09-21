CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS policy_chunks (
  chunk_id TEXT PRIMARY KEY,
  policy_id TEXT NOT NULL,
  title TEXT NOT NULL,
  section TEXT,
  version TEXT,
  effective_date DATE,
  source_path TEXT NOT NULL,
  content TEXT NOT NULL,
  snippet TEXT NOT NULL,
  embedding vector(384),
  index_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
  employee_id TEXT PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  department TEXT NOT NULL,
  job_title TEXT NOT NULL,
  employment_type TEXT NOT NULL,
  location TEXT NOT NULL,
  hire_date DATE NOT NULL,
  manager_id TEXT,
  employment_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pto_balances (
  employee_id TEXT PRIMARY KEY REFERENCES employees(employee_id),
  pto_type TEXT NOT NULL,
  available_hours INTEGER NOT NULL,
  accrual_rate_hours NUMERIC NOT NULL,
  as_of_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS benefits (
  employee_id TEXT PRIMARY KEY REFERENCES employees(employee_id),
  medical_plan TEXT,
  dental_plan TEXT,
  vision_plan TEXT,
  retirement_enrollment BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL,
  as_of_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS mock_hr_tickets (
  ticket_id TEXT PRIMARY KEY,
  employee_id TEXT REFERENCES employees(employee_id),
  topic TEXT NOT NULL,
  summary TEXT NOT NULL,
  status TEXT NOT NULL,
  mock_action BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
