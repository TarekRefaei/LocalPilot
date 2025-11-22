import type { AcceptanceCriterion, FileRef, PlanStep } from '../models/plan';

export interface ParsedPlanDraft {
  steps: PlanStep[];
  acceptance: AcceptanceCriterion[];
}

function genId(): string {
  return String(Date.now()) + '-' + Math.random().toString(36).slice(2, 8);
}

export function parsePlanDraft(prompt?: string): ParsedPlanDraft {
  if (!prompt?.trim()) return { steps: [], acceptance: [] };
  const lines = prompt.split(/\r?\n/).map((l) => l.trim());

  const steps: PlanStep[] = [];
  const acceptance: AcceptanceCriterion[] = [];

  let inAcceptance = false;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;

    if (/^acceptance[:\-\s]?/i.test(line)) {
      inAcceptance = true;
      continue;
    }

    if (inAcceptance) {
      if (/^[-*]\s+/.test(line)) {
        const { text, refs } = extractCriterion(line.replace(/^[-*]\s+/, ''));
        const item: AcceptanceCriterion = { id: genId(), text, done: false };
        if (refs?.length) item.refs = refs;
        acceptance.push(item);
      }
      continue;
    }

    // Steps: lines like "1. Do X" or "- Do X"
    const mNum = line.match(/^\d+[.)]\s+(.*)$/);
    const mDash = line.match(/^[-*]\s+(.*)$/);
    const title = mNum?.[1] ?? mDash?.[1];
    if (title) {
      steps.push({ id: genId(), title: title.trim(), done: false, order: steps.length });
    }
  }

  return { steps, acceptance };
}

function extractCriterion(text: string): { text: string; refs?: FileRef[] } {
  const refs: FileRef[] = [];
  // Parse [file: path#start-end] optional ranges
  const refRegex = /\[file:\s*([^\]#]+)(?:#(\d+)(?:-(\d+))?)?\]/gi;
  let cleaned = text;
  let m: RegExpExecArray | null;
  while ((m = refRegex.exec(text))) {
    const path = (m[1] ?? '').trim();
    const start = m[2] ? parseInt(m[2], 10) : undefined;
    const end = m[3] ? parseInt(m[3], 10) : undefined;
    const ref: FileRef = {
      path,
      ...(typeof start === 'number' ? { startLine: start } : {}),
      ...(typeof end === 'number' ? { endLine: end } : {}),
    };
    refs.push(ref);
    cleaned = cleaned.replace(m[0] ?? '', '').trim();
  }
  return refs.length ? { text: cleaned.trim(), refs } : { text: cleaned.trim() };
}
