import { SERVER_BASE_URL } from '../../config/server.config';
const API_BASE = `${SERVER_BASE_URL}/api`;

export async function startExecution(payload: { planId: string; markdown: string ; workspaceRoot: string}) {
  return post(`/execute_v2/plan`, {
    plan: JSON.parse(payload.markdown.match(/\{[\s\S]*\}/)?.[0] ?? "{}"),
    workspace_root: payload.workspaceRoot,
    model: "qwen2.5-coder:7b-instruct-q4_K_M",
  });
}

export async function applyDiff(executionId: string) {
  return post(`/execute_v2/${executionId}/apply`);
}

export async function reindex(executionId: string) {
  return post(`/execute_v2/${executionId}/reindex`);
}


export async function nextTask(executionId: string) {
  return post(`/execute_v2/${executionId}/next`);
}

export async function resumeExecution(executionId: string) {
  return post(`/execute_v2/${executionId}/resume`);
}

export async function skipTask(executionId: string) {
  return post(`/execute_v2/${executionId}/skip`);
}

export async function retryTask(executionId: string) {
  return post(`/execute_v2/${executionId}/retry`);
}

export async function getExecution(executionId: string) {
  return get(`/execute_v2/${executionId}`);
}

async function post(path: string, body?: any) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}

async function get(path: string) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}
