export async function checkServerHealth(): Promise<boolean> {
  const res = await fetch('http://localhost:52741/health');
  return res.ok;
}
