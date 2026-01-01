const API = 'http://localhost:8000/api';

export async function startExecution(payload: { planId: string; plan: any; workspaceRoot: string}) {
  // Backend expects a normalized, approved plan object bound to planId.
  return post(`/execute/plan`, payload);
}

export async function applyDiff(executionId: string) {
  return post(`/execute/${executionId}/apply`);
}

export async function reindex(executionId: string) {
  return post(`/execute/${executionId}/reindex`);
}

export async function getExecution(executionId: string) {
  return get(`/execute/${executionId}`);
}

export async function prepareTask(executionId: string, taskId: string) {
  return post(`/execute/${executionId}/prepare/${taskId}`);
}

export async function invokeTask(executionId: string, taskId: string) {
  return post(`/execute/${executionId}/invoke/${taskId}`);
}

async function post(path: string, body?: any) {
  const res = await fetch(API + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}

async function get(path: string) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}
