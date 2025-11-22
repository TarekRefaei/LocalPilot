import { isApplyAllowed, isSafeCreate, truncateUnifiedDiff } from '@/services/actPolicy';

describe('Act Policy - apply safety', () => {
  it('strict: requires git repo and clean tree', () => {
    expect(isApplyAllowed('strict', true, false)).toBe(true);
    expect(isApplyAllowed('strict', false, false)).toBe(false);
    expect(isApplyAllowed('strict', true, true)).toBe(false);
  });

  it('git-optional: allows outside git but still requires clean tree when in git', () => {
    expect(isApplyAllowed('git-optional', false, false)).toBe(true);
    expect(isApplyAllowed('git-optional', true, false)).toBe(true);
    expect(isApplyAllowed('git-optional', true, true)).toBe(false);
  });

  it('unsafe: allows both outside git and dirty tree', () => {
    expect(isApplyAllowed('unsafe', false, false)).toBe(true);
    expect(isApplyAllowed('unsafe', true, true)).toBe(true);
  });
});

describe('Act Policy - auto-approve safe creates', () => {
  it('auto-approves creates under docs/** and tests/** and .localpilot/**', () => {
    expect(isSafeCreate('docs/readme.md', { safeCreates: true })).toBe(true);
    expect(isSafeCreate('docs/guide.rst', { safeCreates: true })).toBe(true);
    expect(isSafeCreate('tests/unit/foo.test.ts', { safeCreates: true })).toBe(true);
    expect(isSafeCreate('__tests__/bar.spec.ts', { safeCreates: true })).toBe(true);
    expect(isSafeCreate('.localpilot/audit/2025-01-01.diff', { safeCreates: true })).toBe(true);
  });

  it('does not auto-approve outside safe locations or for unknown extensions', () => {
    expect(isSafeCreate('src/index.ts', { safeCreates: true })).toBe(false);
    expect(isSafeCreate('README.md', { safeCreates: true })).toBe(false);
    expect(isSafeCreate('docs/image.png', { safeCreates: true })).toBe(false);
  });

  it('respects disabling safe creates', () => {
    expect(isSafeCreate('docs/readme.md', { safeCreates: false })).toBe(false);
  });
});

describe('Act Policy - diff truncation', () => {
  function makeDiffLines(n: number): string[] {
    const lines: string[] = [];
    lines.push('diff --git a/file.txt b/file.txt');
    lines.push('--- a/file.txt');
    lines.push('+++ b/file.txt');
    lines.push('@@');
    for (let i = 0; i < n; i++) {
      lines.push(`+ line ${i}`);
    }
    return lines;
  }

  it('truncates per-file and total line counts and appends marker', () => {
    const diff = makeDiffLines(1000).join('\n');
    const truncated = truncateUnifiedDiff(diff, { maxLinesPerFile: 300, maxTotalLines: 2000 });
    const count = truncated.split('\n').length;
    expect(count).toBeLessThanOrEqual(300 + 10); // header + marker margin
    expect(truncated).toContain('...diff truncated');
  });

  it('does not truncate small diffs', () => {
    const diff = makeDiffLines(10).join('\n');
    const truncated = truncateUnifiedDiff(diff, { maxLinesPerFile: 300, maxTotalLines: 2000 });
    expect(truncated).toBe(diff);
  });
});
