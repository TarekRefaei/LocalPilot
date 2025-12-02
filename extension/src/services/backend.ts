import * as vscode from 'vscode';
import { randomUUID as nodeRandomUUID } from 'crypto';

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

export async function fetchAvailableModels(): Promise<string[]> {
  const cfg = vscode.workspace.getConfiguration('localpilot');
  const baseUrl = String(cfg.get('backend.baseUrl') ?? 'http://127.0.0.1:8765');
  const url = `${baseUrl.replace(/\/$/, '')}/api/models`;
  try {
    const res = await fetch(url, { method: 'GET' });
    if (!res.ok) return [];
    const body: unknown = await res.json();
    // body can be either an array of strings/objects or an object with a models array
    const extractNames = (arr: unknown[]): string[] => {
      const out: string[] = [];
      for (const it of arr) {
        if (typeof it === 'string') {
          out.push(it);
        } else if (typeof it === 'object' && it !== null) {
          const o = it as { name?: unknown; id?: unknown };
          const val =
            typeof o.name === 'string' ? o.name : typeof o.id === 'string' ? o.id : undefined;
          if (val) out.push(val);
        }
      }
      return out;
    };
    if (Array.isArray(body)) {
      return extractNames(body);
    }
    if (typeof body === 'object' && body !== null) {
      const maybe = body as { models?: unknown };
      if (Array.isArray(maybe.models)) {
        return extractNames(maybe.models);
      }
    }
    return [];
  } catch (err) {
    console.warn('[LocalPilot] fetchAvailableModels failed', err);
    return [];
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

let lastRequestId: string | null = null;

export function getLastRequestId(): string | null {
  return lastRequestId;
}

export async function streamChatFromBackend(
  prompt: string,
  abort: AbortSignal,
  cbs: StreamCallbacks,
  sessionId?: string
): Promise<void> {
  const cfg = vscode.workspace.getConfiguration('localpilot');
  const baseUrl = String(cfg.get('backend.baseUrl') ?? 'http://127.0.0.1:8765');
  const model = String(cfg.get('defaultModel') ?? cfg.get('model') ?? 'local');

  const url = `${baseUrl.replace(/\/$/, '')}/chat/stream`;
  log('info', `Starting stream to ${url} with model=${model}`);
  try {
    cbs.onStart?.();
    // generate a request id client-side
    const rid =
      typeof nodeRandomUUID === 'function' ? nodeRandomUUID() : Math.random().toString(36).slice(2);
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, model, request_id: rid, session_id: sessionId }),
      signal: abort,
    });
    if (!res.ok || !res.body) {
      const msg = `Backend returned ${res.status}`;
      log('error', msg);
      throw new Error(msg);
    }
    // capture request id from headers if provided
    const hdrRid = res.headers.get('X-Request-Id');
    lastRequestId = hdrRid ?? rid;
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

export async function abortLastRequest(): Promise<boolean> {
  try {
    const rid = lastRequestId;
    if (!rid) return false;
    const cfg = vscode.workspace.getConfiguration('localpilot');
    const baseUrl = String(cfg.get('backend.baseUrl') ?? 'http://127.0.0.1:8765');
    const url = `${baseUrl.replace(/\/$/, '')}/chat/abort`;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: rid }),
    });
    return res.ok;
  } catch (e) {
    log('warn', 'abortLastRequest failed', e);
    return false;
  }
}

export interface HistoryItem {
  role: string;
  text: string;
  ts: number;
}

export async function fetchHistory(sessionId: string, limit = 200): Promise<HistoryItem[]> {
  const cfg = vscode.workspace.getConfiguration('localpilot');
  const baseUrl = String(cfg.get('backend.baseUrl') ?? 'http://127.0.0.1:8765');
  const url = `${baseUrl.replace(/\/$/, '')}/chat/history?session_id=${encodeURIComponent(sessionId)}&limit=${limit}`;
  try {
    const res = await fetch(url, { method: 'GET' });
    if (!res.ok) return [];
    const body: unknown = await res.json();
    if (typeof body === 'object' && body !== null) {
      const maybe = body as { history?: unknown };
      if (Array.isArray(maybe.history)) {
        const result: HistoryItem[] = [];
        for (const m of maybe.history) {
          if (typeof m === 'object' && m !== null && 'role' in m && 'text' in m && 'ts' in m) {
            const { role, text, ts } = m as { role: unknown; text: unknown; ts: unknown };
            if (typeof role === 'string' && typeof text === 'string' && typeof ts === 'number') {
              result.push({ role, text, ts });
            }
          }
        }
        return result;
      }
    }
    return [];
  } catch (e) {
    log('warn', 'fetchHistory failed', e);
    return [];
  }
}
