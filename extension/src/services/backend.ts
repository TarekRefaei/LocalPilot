import * as vscode from 'vscode';

const LOG_PREFIX = '[LocalPilot Chat]';

function log(level: 'info' | 'warn' | 'error', message: string, data?: unknown): void {
  const msg = `${LOG_PREFIX} ${message}`;
  if (level === 'error') {
    console.error(msg, data);
  } else if (level === 'warn') {
    console.warn(msg, data);
  } else {
    console.log(msg, data);
  }
}

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
  log('info', `Starting stream to ${url} with model=${model}`);
  try {
    cbs.onStart?.();
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, model }),
      signal: abort,
    });
    if (!res.ok || !res.body) {
      const msg = `Backend returned ${res.status}`;
      log('error', msg);
      throw new Error(msg);
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
    log('info', 'Stream completed successfully');
    cbs.onEnd?.();
  } catch (err) {
    if (
      typeof err === 'object' &&
      err !== null &&
      'name' in err &&
      (err as { name?: string }).name === 'AbortError'
    ) {
      log('info', 'Stream aborted by user');
      return;
    }
    const errMsg = err instanceof Error ? err.message : String(err);
    log('error', `Stream failed: ${errMsg}`);
    cbs.onError?.(err);
  }
}
