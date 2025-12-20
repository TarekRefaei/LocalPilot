export async function checkServerHealth(): Promise<boolean> {
  const res = await fetch('http://localhost:8000/health');
  return res.ok;
}

export async function checkOllamaHealth(): Promise<boolean> {
  try {
    const res = await fetch('http://localhost:8000/health/ollama');
    const json = await res.json();
    return json.status === 'ok';
  } catch {
    return false;
  }
}

export async function getProjectSummary(projectId: string): Promise<any> {
  const res = await fetch(`http://localhost:8000/api/project/${encodeURIComponent(projectId)}/summary`);
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
