import type { Plan } from '../../core/entities/plan.entity';
import type { Task } from '../../core/entities/task.entity';
import type { PlanSchema, TaskSchema } from '../../core/schemas/plan.schema';

export interface ParseResult {
  markdown: string;
  plan: Plan | null;
}

export function parsePlanMarkdown(markdown: string): ParseResult {
  try {
    const json = extractJsonBlock(markdown || '');
    if (!json) return { markdown, plan: null };
    const data = JSON.parse(json) as PlanSchema;
    if (!isValidPlanSchema(data)) return { markdown, plan: null };
    const plan: Plan = {
      id: data.id,
      title: data.title,
      overview: data.overview,
      tasks: data.tasks.map(mapTask),
      status: 'draft',
    };
    return { markdown, plan };
  } catch {
    return { markdown, plan: null };
  }
}

function extractJsonBlock(markdown: string): string | null {
  // Prefer ```json fenced block explicitly
  const jsonFence = /```json\s*([\s\S]*?)```/i;
  const m = jsonFence.exec(markdown);
  if (m && m[1]) {
    return m[1].trim();
  }

  // Fallback: try to locate a raw JSON object
  const start = markdown.indexOf('{');
  const end = markdown.lastIndexOf('}');
  if (start !== -1 && end !== -1 && end > start) {
    const candidate = markdown.slice(start, end + 1).trim();
    if (candidate.startsWith('{')) return candidate;
  }

  return null;
}

function isValidPlanSchema(p: any): p is PlanSchema {
  return (
    p &&
    typeof p.id === 'string' &&
    typeof p.title === 'string' &&
    typeof p.overview === 'string' &&
    p.status === 'draft' &&
    Array.isArray(p.tasks) &&
    p.tasks.every(isValidTaskSchema)
  );
}

function isValidTaskSchema(t: any): t is TaskSchema {
  return (
    t &&
    typeof t.id === 'string' &&
    typeof t.orderIndex === 'number' &&
    typeof t.title === 'string' &&
    typeof t.description === 'string' &&
    typeof t.filePath === 'string' &&
    (t.actionType === 'create' || t.actionType === 'modify' || t.actionType === 'delete') &&
    Array.isArray(t.details) && t.details.every((d: any) => typeof d === 'string') &&
    Array.isArray(t.dependencies) && t.dependencies.every((d: any) => typeof d === 'string')
  );
}

function mapTask(t: TaskSchema): Task {
  return {
    id: t.id,
    orderIndex: t.orderIndex,
    title: t.title,
    description: t.description,
    filePath: t.filePath,
    actionType: t.actionType,
    details: t.details,
    dependencies: t.dependencies,
  };
}
