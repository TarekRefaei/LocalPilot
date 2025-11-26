describe('LocalPilot Commands: toggle and add branches', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('toggles a step and adds a step at default index', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');
    const { createPlan } = await import('@/models/plan');

    const plan = createPlan({ id: 'p1', title: 'T' });
    plan.steps = [
      { id: 's1', title: 'A', order: 0, done: false },
      { id: 's2', title: 'B', order: 1, done: false },
    ];

    const store = [JSON.parse(JSON.stringify(plan))];
    const state = {
      getPlans: jest.fn(() => store.map((p) => JSON.parse(JSON.stringify(p)))),
      setPlans: jest.fn((next: any[]) => {
        store.splice(0, store.length, ...next);
      }),
    } as any;

    type Disposable = { dispose: () => void };
    const context = { subscriptions: [] as Disposable[] } as any;
    registerLocalPilotCommands(context, state);

    const regCalls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handlers = new Map<string, Function>(regCalls.map(([id, fn]) => [id, fn]));

    // Toggle step
    await handlers.get(COMMAND_IDS.planStepToggle)!({ planId: 'p1', stepId: 's1' });
    const afterToggle = store[0];
    expect(afterToggle.steps.find((s: any) => s.id === 's1')!.done).toBe(true);

    // Add step without explicit index (default to end)
    await handlers.get(COMMAND_IDS.planStepAdd)!({ planId: 'p1', title: 'C' });
    const afterAdd = store[0];
    expect(afterAdd.steps.length).toBe(3);
    expect(afterAdd.steps.map((s: any) => s.order)).toEqual([0, 1, 2]);
  });
});
