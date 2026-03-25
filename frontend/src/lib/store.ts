import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface EvaluationResult {
  project_id?: number;
  evaluation_id?: number;
  status?: string;
  overall_score?: number;
  comprehensive_analysis?: Record<string, unknown>;
  message?: string;

  // From /evaluations/:id
  id?: number;
  code_quality_score?: number;
  functionality_score?: number;
  documentation_score?: number;
  innovation_score?: number;
  feedback?: string;
  strengths?: string[];
  weaknesses?: string[];
  recommendations?: string[];
  ai_model_used?: string;
  evaluation_time?: number;
  created_at?: string;
}

export interface Project {
  id: number;
  name: string;
  student_name: string;
  student_email?: string;
  submission_type: string;
  github_url?: string;
  file_path?: string;
  created_at: string;
}

export interface ProgressEvent {
  type: 'progress' | 'complete' | 'error' | 'heartbeat';
  stage?: string;
  message?: string;
  percent?: number;
  data?: EvaluationResult;
}

export interface OverviewStats {
  total_projects: number;
  total_evaluations: number;
  average_score: number;
  recent_evaluations: EvaluationResult[];
  submission_type_counts?: Record<string, number>;
}

// ─── Store ────────────────────────────────────────────────────────────────────

interface AuroraState {
  // Evaluations
  evaluations: EvaluationResult[];
  currentEvaluation: EvaluationResult | null;
  setEvaluations: (evals: EvaluationResult[]) => void;
  setCurrentEvaluation: (ev: EvaluationResult | null) => void;
  addEvaluation: (ev: EvaluationResult) => void;

  // Projects
  projects: Project[];
  setProjects: (projects: Project[]) => void;

  // Stats
  stats: OverviewStats | null;
  setStats: (stats: OverviewStats) => void;

  // Progress (live WebSocket)
  progress: ProgressEvent | null;
  progressStage: string;
  progressPercent: number;
  setProgress: (event: ProgressEvent) => void;
  resetProgress: () => void;

  // Loading states
  isSubmitting: boolean;
  isLoadingHistory: boolean;
  isLoadingStats: boolean;
  setIsSubmitting: (v: boolean) => void;
  setIsLoadingHistory: (v: boolean) => void;
  setIsLoadingStats: (v: boolean) => void;

  // Error
  error: string | null;
  setError: (msg: string | null) => void;
}

export const useAuroraStore = create<AuroraState>()(
  persist(
    (set) => ({
      // Evaluations
      evaluations: [],
      currentEvaluation: null,
      setEvaluations: (evaluations) => set({ evaluations }),
      setCurrentEvaluation: (currentEvaluation) => set({ currentEvaluation }),
      addEvaluation: (ev) =>
        set((state) => ({ evaluations: [ev, ...state.evaluations] })),

      // Projects
      projects: [],
      setProjects: (projects) => set({ projects }),

      // Stats
      stats: null,
      setStats: (stats) => set({ stats }),

      // Progress
      progress: null,
      progressStage: '',
      progressPercent: 0,
      setProgress: (event) =>
        set({
          progress: event,
          progressStage: event.stage || '',
          progressPercent: event.percent || 0,
        }),
      resetProgress: () =>
        set({ progress: null, progressStage: '', progressPercent: 0 }),

      // Loading
      isSubmitting: false,
      isLoadingHistory: false,
      isLoadingStats: false,
      setIsSubmitting: (isSubmitting) => set({ isSubmitting }),
      setIsLoadingHistory: (isLoadingHistory) => set({ isLoadingHistory }),
      setIsLoadingStats: (isLoadingStats) => set({ isLoadingStats }),

      // Error
      error: null,
      setError: (error) => set({ error }),
    }),
    {
      name: 'aurora-storage',
      partialize: (state) => ({
        evaluations: state.evaluations.slice(0, 20), // persist last 20
        stats: state.stats,
      }),
    }
  )
);
