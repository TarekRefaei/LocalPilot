describe('LocalPilot Commands: additional branch coverage', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('showViews opens container and shows info', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS, VIEW_CONTAINER_ID } = await import('@/ids');

    const context = { subscriptions: [] as any[] } as any;
    registerLocalPilotCommands(context, undefined as any);

    const calls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handler = new Map<string, Function>(calls.map(([id, fn]) => [id, fn]));

    await handler.get(COMMAND_IDS.showViews)!();
    expect(vscode.commands.executeCommand).toHaveBeenCalledWith(
      'setContext',
      'localpilot.views.visible',
      true,
    );
    expect(
      (vscode.commands.executeCommand as any).mock.calls.some((c: any[]) =>
        String(c[0]).includes(`workbench.view.extension.${VIEW_CONTAINER_ID}`),
      ),
    ).toBe(true);
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith('LocalPilot views opened');
  });

  it('focusChatInput success path shows info', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');

    // First executeCommand resolves to simulate success opening
    (vscode.commands.executeCommand as any).mockImplementation(() => Promise.resolve(undefined));

    const context = { subscriptions: [] as any[] } as any;
    registerLocalPilotCommands(context, undefined as any);
    const calls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handler = new Map<string, Function>(calls.map(([id, fn]) => [id, fn]));

    await handler.get(COMMAND_IDS.focusChatInput)!();
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith(
      'Focus Chat input (LocalPilot)',
    );
  });

  it('planCreate clamps steps to [0,10]', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');

    const store: any[] = [];
    const state = {
      getPlans: jest.fn(() => store.map((p) => JSON.parse(JSON.stringify(p)))),
      setPlans: jest.fn((next: any[]) => {
        store.splice(0, store.length, ...next);
      }),
    } as any;
    const context = { subscriptions: [] as any[] } as any;
    registerLocalPilotCommands(context, state);
    const calls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handler = new Map<string, Function>(calls.map(([id, fn]) => [id, fn]));

    // Negative -> 0 steps
    await handler.get(COMMAND_IDS.planCreate)!({ id: 'pneg', title: 'N', steps: -5 });
    expect(store.length).toBe(1);
    expect(Array.isArray(store[0].steps)).toBe(true);
    expect(store[0].steps.length).toBe(0);

    // Over max -> 10 steps
    await handler.get(COMMAND_IDS.planCreate)!({ id: 'pmax', title: 'M', steps: 15 });
    expect(store.length).toBe(2);
    expect(store[1].steps.length).toBe(10);
  });
});
