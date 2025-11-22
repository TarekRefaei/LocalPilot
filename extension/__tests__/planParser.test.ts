/// <reference types="jest" />

describe('parsePlanDraft', () => {
  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('parses numbered and dashed steps plus acceptance criteria with file refs', async () => {
    const { parsePlanDraft } = await import('@/services/planParser');

    const prompt = [
      'Implement feature X',
      '1. Setup state',
      '2. Render UI',
      '- Wire commands',
      'Acceptance:',
      '- Verify state persisted [file: src/services/state.ts#50-90]',
      '- Ensure UI renders steps [file: src/views/providers.ts]'
    ].join('\n');

    const result = parsePlanDraft(prompt);

    // Steps
    expect(Array.isArray(result.steps)).toBe(true);
    expect(result.steps.length).toBe(3);
    expect(result.steps[0]!.title).toBe('Setup state');
    expect(result.steps[1]!.order).toBe(1);
    expect(result.steps[2]!.title).toBe('Wire commands');

    // Acceptance
    expect(Array.isArray(result.acceptance)).toBe(true);
    expect(result.acceptance.length).toBe(2);
    const a0 = result.acceptance[0]!;
    expect(a0.text).toBe('Verify state persisted');
    expect(a0.refs?.[0]?.path).toContain('src/services/state.ts');
    expect(a0.refs?.[0]?.startLine).toBe(50);
    expect(a0.refs?.[0]?.endLine).toBe(90);

    const a1 = result.acceptance[1]!;
    expect(a1.text).toBe('Ensure UI renders steps');
    expect(a1.refs?.[0]?.path).toContain('src/views/providers.ts');
  });

  it('returns empty when prompt is empty', async () => {
    const { parsePlanDraft } = await import('@/services/planParser');
    const result = parsePlanDraft('');
    expect(result.steps.length).toBe(0);
    expect(result.acceptance.length).toBe(0);
  });
});
