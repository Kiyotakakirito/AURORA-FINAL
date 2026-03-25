-- ============================================================
-- AURORA — Supabase Schema Migration
-- Run this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- 1. Projects table
CREATE TABLE IF NOT EXISTS public.projects (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    student_name    VARCHAR(255)    NOT NULL,
    student_email   VARCHAR(255),
    submission_type VARCHAR(20)     NOT NULL,   -- 'zip', 'github', 'pdf'
    file_path       VARCHAR(500),               -- path to uploaded project file
    pdf_path        VARCHAR(500),               -- path to PDF report
    github_url      VARCHAR(500),
    created_at      TIMESTAMPTZ     DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     DEFAULT NOW()
);

-- 2. Evaluations table
CREATE TABLE IF NOT EXISTS public.evaluations (
    id                      SERIAL PRIMARY KEY,
    project_id              INTEGER         NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    overall_score           FLOAT           NOT NULL,
    max_score               INTEGER         DEFAULT 100,

    -- Detailed scores
    code_quality_score      FLOAT,
    functionality_score     FLOAT,
    documentation_score     FLOAT,
    innovation_score        FLOAT,

    -- JSON analysis results
    code_analysis           JSONB,
    report_analysis         JSONB,
    comprehensive_analysis  JSONB,
    feedback                TEXT,
    strengths               JSONB,
    weaknesses              JSONB,
    recommendations         JSONB,

    -- Metadata
    ai_model_used           VARCHAR(100),
    evaluation_time         FLOAT,              -- seconds
    created_at              TIMESTAMPTZ     DEFAULT NOW()
);

-- 3. Evaluation criteria table
CREATE TABLE IF NOT EXISTS public.evaluation_criteria (
    id                      SERIAL PRIMARY KEY,
    name                    VARCHAR(255)    NOT NULL,
    description             TEXT,

    -- Weights (should sum to 1.0)
    code_quality_weight     FLOAT           DEFAULT 0.3,
    functionality_weight    FLOAT           DEFAULT 0.4,
    documentation_weight    FLOAT           DEFAULT 0.2,
    innovation_weight       FLOAT           DEFAULT 0.1,

    max_score               INTEGER         DEFAULT 100,
    rubric_details          JSONB,

    is_active               BOOLEAN         DEFAULT TRUE,
    created_at              TIMESTAMPTZ     DEFAULT NOW(),
    updated_at              TIMESTAMPTZ     DEFAULT NOW()
);

-- ============================================================
-- Row Level Security (RLS)
-- Allow full access via the service-role key used by the backend
-- If you use the anon key, enable these policies instead.
-- ============================================================
ALTER TABLE public.projects            ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evaluations         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evaluation_criteria ENABLE ROW LEVEL SECURITY;

-- Allow ALL operations for authenticated requests (service-role key bypasses RLS automatically)
-- Uncomment the lines below ONLY if you are using the anon key in SUPABASE_KEY:
/*
CREATE POLICY "Allow all for anon" ON public.projects            FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON public.evaluations         FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON public.evaluation_criteria FOR ALL USING (true) WITH CHECK (true);
*/

-- ============================================================
-- Optional: auto-update updated_at on projects
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER trg_projects_updated_at
    BEFORE UPDATE ON public.projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_evaluation_criteria_updated_at
    BEFORE UPDATE ON public.evaluation_criteria
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
