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
