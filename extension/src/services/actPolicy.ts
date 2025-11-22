export type ApplySafety = 'strict' | 'git-optional' | 'unsafe';

export function isApplyAllowed(
  safety: ApplySafety,
  inGitRepo: boolean,
  hasUncommittedChanges: boolean
): boolean {
  if (safety === 'unsafe') return true;
  if (safety === 'git-optional') {
    if (!inGitRepo) return true;
    return !hasUncommittedChanges;
  }
  // strict
  return inGitRepo && !hasUncommittedChanges;
}

export function isSafeCreate(
  filePath: string,
  opts: { safeCreates: boolean }
): boolean {
  if (!opts.safeCreates) return false;
  const p = filePath.replace(/\\/g, '/');
  const lower = p.toLowerCase();

  // .localpilot/**
  if (lower.startsWith('.localpilot/')) return true;

  // docs/** with allowed extensions
  if (lower.startsWith('docs/')) {
    const allowed = ['.md', '.mdx', '.txt', '.rst'];
    return allowed.some((ext) => lower.endsWith(ext));
  }

  // tests/** or __tests__/** with *.test.* or *.spec.*
  const isTestsDir =
    lower.startsWith('tests/') ||
    lower.startsWith('__tests__/') ||
    lower.includes('/__tests__/');
  if (isTestsDir) {
    return /\.(test|spec)\./.test(lower);
  }

  return false;
}

export function truncateUnifiedDiff(
  diff: string,
  opts: { maxLinesPerFile: number; maxTotalLines: number }
): string {
  const { maxLinesPerFile, maxTotalLines } = opts;
  const lines = diff.split(/\r?\n/);
  const out: string[] = [];
  let total = 0;
  let fileLineCount = 0;

  const push = (line: string) => {
    out.push(line);
    total += 1;
  };

  let inFile = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i] ?? '';

    // Start of a new file diff (best-effort detection)
    if (line.startsWith('diff --git ') || line.startsWith('--- ') || line.startsWith('Index: ')) {
      inFile = true;
      fileLineCount = 0;
    }

    if (total >= maxTotalLines) {
      push('...diff truncated (total limit)');
      break;
    }

    if (inFile && fileLineCount >= maxLinesPerFile) {
      // Skip until next file boundary, but add a marker once
      if (out[out.length - 1] !== '...diff truncated (file limit)') {
        push('...diff truncated (file limit)');
      }
      // Continue scanning for next file header without appending
      continue;
    }

    push(line);
    if (inFile) fileLineCount += 1;
  }

  return out.join('\n');
}
