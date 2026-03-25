import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 120_000, // 2 min — AI eval can take time
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('aurora_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Global error handler
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      err.message ||
      'An unexpected error occurred';
    return Promise.reject(new Error(msg));
  }
);

// ─── API Methods ──────────────────────────────────────────────────────────────

export const submitProject = (formData: FormData) =>
  api.post('/submit/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 300_000, // 5 min for full eval
  });

export const getOverviewStats = () =>
  api.get('/stats/overview');

export const listProjects = (skip = 0, limit = 50) =>
  api.get('/projects/', { params: { skip, limit } });

export const getProject = (id: number) =>
  api.get(`/projects/${id}`);

export const listEvaluations = (skip = 0, limit = 50) =>
  api.get('/evaluations/', { params: { skip, limit } });

export const getEvaluation = (id: number) =>
  api.get(`/evaluations/${id}`);

export const getProjectEvaluations = (projectId: number) =>
  api.get(`/projects/${projectId}/evaluations`);

export const listCriteria = () =>
  api.get('/criteria/');

export const createCriteria = (data: Record<string, unknown>) =>
  api.post('/criteria/', data);

export const getAIStatus = () =>
  api.get('/ai/status');

// ─── WebSocket Factory ────────────────────────────────────────────────────────

const WS_BASE = (process.env.REACT_APP_API_URL || 'http://localhost:8000')
  .replace(/^http/, 'ws')
  .replace('/api/v1', '');

export const createEvaluationSocket = (jobId: string): WebSocket => {
  return new WebSocket(`${WS_BASE}/ws/evaluate/${jobId}`);
};
