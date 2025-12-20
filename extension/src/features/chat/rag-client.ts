export type RetrievedChunk = {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance: number;
};

export async function queryRAG(
  projectId: string,
  text: string,
  topK: number = 5,
  filters?: Record<string, any>
): Promise<RetrievedChunk[]> {
  const res = await fetch("http://localhost:8000/api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project_id: projectId,
      query: text,
      top_k: topK,
      filters: filters ?? null
    })
  });

  if (!res.ok) {
    let detail = "";
    try {
      detail = await res.text();
    } catch {}
    throw new Error(`RAG query failed: ${res.status} ${detail}`);
  }

  const json = await res.json();
  return (json && Array.isArray(json.chunks)) ? json.chunks as RetrievedChunk[] : [];
}
