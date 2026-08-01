import { SERVER_BASE_URL } from '../../config/server.config';

export async function requestPlanRefinement(plan: any, structuralIssues: any[]) {
  const res = await fetch(`${SERVER_BASE_URL}/api/plan/refine`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan, structuralIssues }),
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
