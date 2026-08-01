import { SERVER_BASE_URL } from '../../config/server.config';

export interface StructuralIssue {
  code: string;
  message: string;
  level: 'error' | 'warning';
  taskId?: string;
}

export async function analyzePlanStructure(plan: any): Promise<StructuralIssue[]> {
  const res = await fetch(`${SERVER_BASE_URL}/api/plan/structure/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan }),
  });

  if (!res.ok) {
    return [];
  }

  const json = await res.json().catch(() => null);
  return json?.issues ?? [];
}
