interface GeneratePlanRequest {
  projectId: string;
  messages: any[];
}

export async function generatePlan(
  req: GeneratePlanRequest
): Promise<string> {
  const res = await fetch('http://localhost:8000/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      project_id: req.projectId,
      model: 'qwen2.5-coder:7b-instruct-q4_K_M',
      messages: req.messages,
    }),
  });

  if (!res.ok) {
    throw new Error(`Plan API failed (${res.status})`);
  }

  const data = await res.json();
  return data.markdown as string;
}
