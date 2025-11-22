/// <reference types="jest" />

describe('Plan model, commands, and PlansTreeDataProvider', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('supports CRUD via commands and renders nested steps in the Plans view', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { PlansTreeDataProvider } = await import('@/views/providers');
    const { InMemoryState } = await import('@/services/state');
    const { COMMAND_IDS } = await import('@/ids');

    const state = new InMemoryState();

    type Disposable = { dispose: () => void };
    const context = { subscriptions: [] as Disposable[] } as any;

    registerLocalPilotCommands(context, state);

    // Access registered handlers
    const handlers = new Map<string, Function>(
      Object.entries((vscode.commands as any).__getRegistered()) as [string, Function][]
    );

    // Create a plan with 2 steps
    await handlers.get(COMMAND_IDS.planCreate)!({ title: 'Test Plan', steps: 2 });
    const plans1 = state.getPlans();
    expect(plans1.length).toBe(1);
    const p1 = plans1[0]! as any;
    expect(p1.title).toBe('Test Plan');
    expect(p1.steps.length).toBe(2);
    expect(p1.steps[0]!.order).toBe(0);

    // Add a step at index 1
    const planId = p1.id as string;
    await handlers.get(COMMAND_IDS.planStepAdd)!({ planId, title: 'Inserted', index: 1 });
    const plans2 = state.getPlans();
    expect(plans2.length).toBeGreaterThan(0);
    const p2 = plans2[0]! as any;
    expect(p2.steps.length).toBe(3);
    expect(p2.steps[1]!.title).toContain('Inserted');

    // Toggle the inserted step
    const stepId = p2.steps[1]!.id as string;
    await handlers.get(COMMAND_IDS.planStepToggle)!({ planId, stepId });
    const plans3 = state.getPlans();
    const p3 = plans3[0]! as any;
    expect(p3.steps[1]!.done).toBe(true);

    // Move step down
    await handlers.get(COMMAND_IDS.planStepMoveDown)!({ planId, stepId });
    const plans4 = state.getPlans();
    const p4 = plans4[0]! as any;
    const idxAfterDown = p4.steps.findIndex((s: any) => s.id === stepId);
    expect(idxAfterDown).toBe(2);

    // Move step up
    await handlers.get(COMMAND_IDS.planStepMoveUp)!({ planId, stepId });
    const plans5 = state.getPlans();
    const p5 = plans5[0]! as any;
    const idxAfterUp = p5.steps.findIndex((s: any) => s.id === stepId);
    expect(idxAfterUp).toBe(1);

    // Delete step
    await handlers.get(COMMAND_IDS.planStepDelete)!({ planId, stepId });
    const plans6 = state.getPlans();
    const p6 = plans6[0]! as any;
    expect(p6.steps.length).toBe(2);

    // Plans view renders nested steps
    const provider = new PlansTreeDataProvider(state);
    const roots = (await provider.getChildren())!;
    expect(roots.length).toBeGreaterThan(0);
    const planItem = roots[0] as any;
    expect(planItem.contextValue).toBe('plans.plan');
    const stepItems = (await provider.getChildren(planItem)) || [];
    expect(stepItems.length).toBe(p6.steps.length);
    expect((stepItems[0] as any)?.contextValue).toBe('plans.step');
    expect((stepItems[0] as any)?.command?.command).toBe(COMMAND_IDS.planStepToggle);
  });

  it('chat transfer to plan includes prompt and persists via state', async () => {
    const { createChatHandler } = await import('@/chat');
    const { COMMAND_IDS } = await import('@/ids');

    const capturedButtons: any[] = [];
    const state = {
      onDidChange: (() => ({ dispose() {} })) as any,
      getPlans: () => [],
      getIndexingRunning: () => false,
      getRecentPrompts: () => [],
      setPlans: jest.fn(),
      setIndexingRunning: () => {},
      setRecentPrompts: () => {},
    } as any;

    const handler = createChatHandler(state);

    const stream = {
      progress: jest.fn(),
      markdown: jest.fn(),
      button: jest.fn((b: any) => capturedButtons.push(b)),
    } as any;
    const token = { onCancellationRequested: jest.fn(() => ({ dispose() {} })) } as any;

    await handler({ prompt: '1. Do A\n2. Do B\nAcceptance:\n- Verify A [file: a.ts#1-10]' } as any, {} as any, stream, token);

    expect(capturedButtons.length).toBeGreaterThan(0);
    const btn = capturedButtons[0];
    expect(btn.command).toBe(COMMAND_IDS.chatTransferToPlan);
    expect(btn.arguments?.[0]?.prompt).toContain('Acceptance');
  });
});
