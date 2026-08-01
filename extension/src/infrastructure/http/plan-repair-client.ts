export interface PlanRepairRequest {
  plan: any;
  markdown: string;
  blockingWarnings: any[];
  workspace: {
    existingFiles: string[];
  };
}

export async function requestPlanRepair(payload: PlanRepairRequest): Promise<any> {
  const res = await fetch('http://localhost:8000/api/plan/repair', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`plan_repair_failed: ${res.status} ${text}`);
  }

  return await res.json();
}
