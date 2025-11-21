import * as vscode from 'vscode';

export interface StreamCallbacks {
  onStart?: () => void;
  onChunk?: (text: string) => void;
  onEnd?: () => void;
  onError?: (err: unknown) => void;
}

interface ReadResult {
  done?: boolean;
  value?: Uint8Array;
}

export async function streamChatFromBackend(
  prompt: string,
  abort: AbortSignal,
  cbs: StreamCallbacks
): Promise<void> {
  const cfg = vscode.workspace.getConfiguration('localpilot');
  const baseUrl = String(cfg.get('backend.baseUrl') ?? 'http://127.0.0.1:8000');
  const model = String(cfg.get('model') ?? 'local');

  const url = `${baseUrl.replace(/\/$/, '')}/chat/echo`;
  try {
    cbs.onStart?.();
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, model }),
      signal: abort,
    });
    if (!res.ok || !res.body) {
      throw new Error(`Bad response: ${res.status}`);
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let finished = false;
    do {
      const result: ReadResult = await reader.read();
      finished = !!result.done;
      if (result.value) {
        const chunk = decoder.decode(result.value, { stream: true });
        cbs.onChunk?.(chunk);
      }
    } while (!finished);
    cbs.onEnd?.();
  } catch (err) {
    if (
      typeof err === 'object' &&
      err !== null &&
      'name' in err &&
      (err as { name?: string }).name === 'AbortError'
    ) {
      return;
    }
    cbs.onError?.(err);
  }
}
