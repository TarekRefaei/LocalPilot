# Agent 04 — WebSocket Client & Contract

This document captures the current Chat messaging schemas and placeholders for retrieval integration. It is intended to guide Agent 04 in implementing a WS client and aligning message contracts.

## Message Schemas

### Webview → Extension
- refresh
- inlineChat
  - { text: string }
- stop
- regen
- copy
  - { text: string }
- transfer
  - { title: string }
- pickModel

### Extension → Webview
- beginAssistant
- stream
  - { markdown: string }
- endAssistant
- action
  - { command: string; title: string }
- state
  - { plans: number; recent: string[]; model: string }

## Backend Streaming Contract (HTTP, placeholder for WS)
- POST /chat/echo
  - Body: { prompt: string, model?: string }
  - Streamed text/plain response (character chunks)
- Target WS migration: stream token events `{ type: 'token', text }`, terminated by `{ type: 'done' }`.

## Retrieval Interface (Contract Placeholder)
- Future endpoint: POST /retrieve
  - Body: { query: string, topK?: number }
  - Response: { items: Array<{ id: string; title: string; snippet: string; url?: string }> }
- Chat request enrichment: include `retrieval: { items: [...] }` in the conversation context when available.

## Mock Adapters (for tests)

### TypeScript (Webview-level mock)
```ts
export function mockStream(text: string, post: (msg: any) => void) {
  post({ type: 'beginAssistant' });
  for (const ch of text) post({ type: 'stream', markdown: ch });
  post({ type: 'endAssistant' });
}
```

### TypeScript (Retrieval mock)
```ts
export interface RetrievalItem { id: string; title: string; snippet: string; url?: string }
export async function mockRetrieve(query: string): Promise<RetrievalItem[]> {
  return [
    { id: 'doc-1', title: 'Design.md', snippet: `Match for: ${query}` },
  ];
}
```

## Notes
- Current markdown handling is minimal (code fences and line breaks). Agent 04 may improve rendering and references (links, tables, lists).
- No telemetry; keep logging local-only and minimal.
