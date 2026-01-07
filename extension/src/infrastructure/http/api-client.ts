import { SERVER_BASE_URL, API } from '../../config/server.config';

export async function checkServerHealth(): Promise<boolean> {
  const res = await fetch(`${SERVER_BASE_URL}${API.HEALTH}`);
  return res.ok;
}

export async function checkOllamaHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${SERVER_BASE_URL}${API.OLLAMA_HEALTH}`);
    const json = await res.json();
    return json.status === 'ok';
  } catch {
    return false;
  }
}

export async function getProjectSummary(projectId: string): Promise<any> {
  const res = await fetch(`${SERVER_BASE_URL}${API.PROJECT_SUMMARY(projectId)}`);
  if (res.status === 404) {
    throw new Error('summary_not_found');
  }
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`summary_fetch_failed: ${res.status} ${text}`);
  }
  return await res.json();
}

export async function isIndexed(projectId: string): Promise<boolean> {
  try {
    await getProjectSummary(projectId);
    return true;
  } catch (e: any) {
    return false;
  }
}

export async function autoFixPlanPreview(markdown: string, workspaceRoot: string): Promise<{ fixedPlan: any; warnings: string[]; diff: string }>
{
  const res = await fetch(`${SERVER_BASE_URL}${API.PLAN_AUTO_FIX}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ markdown, workspace_root: workspaceRoot }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`auto_fix_failed: ${res.status} ${text}`);
  }
  return await res.json();
}
