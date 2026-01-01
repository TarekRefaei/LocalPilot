import { diffLines } from 'diff';

export function buildPlanFixDiff(before: string, after: string): string {
  const diff = diffLines(before ?? '', after ?? '');
  let out = '';

  diff.forEach(part => {
    const prefix = part.added ? '+' : part.removed ? '-' : ' ';
    out += part.value
      .split('\n')
      .map(line => prefix + line)
      .join('\n');
  });

  return out;
}
