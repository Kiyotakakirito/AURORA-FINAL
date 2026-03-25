-- Run this in Supabase Dashboard → SQL Editor
-- Adds permissive policies so the anon/service key can read and write

CREATE POLICY "allow_all_projects"
    ON public.projects FOR ALL
    USING (true) WITH CHECK (true);

CREATE POLICY "allow_all_evaluations"
    ON public.evaluations FOR ALL
    USING (true) WITH CHECK (true);

CREATE POLICY "allow_all_criteria"
    ON public.evaluation_criteria FOR ALL
    USING (true) WITH CHECK (true);
