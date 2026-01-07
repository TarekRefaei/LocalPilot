export const SERVER_BASE_URL = "http://localhost:8000";

export const API = {
  HEALTH: "/health",
  OLLAMA_HEALTH: "/health/ollama",
  PROJECT_SUMMARY: (id: string) => `/api/project/${encodeURIComponent(id)}/summary`,
  PLAN_AUTO_FIX: "/api/plan/auto-fix",
} as const;
