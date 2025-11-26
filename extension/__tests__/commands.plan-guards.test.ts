describe('LocalPilot Commands: guard branches', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('handles missing ids and early returns without mutating state', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');

    const state = {
      getPlans: jest.fn(() => []),
      setPlans: jest.fn(),
    } as any;

    type Disposable = { dispose: () => void };
    const context = { subscriptions: [] as Disposable[] } as any;
    registerLocalPilotCommands(context, state);

    const regCalls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handlers = new Map<string, Function>(regCalls.map(([id, fn]) => [id, fn]));

    await handlers.get(COMMAND_IDS.planUpdate)!(undefined);
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith('Update Plan');
    expect(state.setPlans).not.toHaveBeenCalled();

    await handlers.get(COMMAND_IDS.planDelete)!(undefined);
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith('Delete Plan');
    expect(state.setPlans).not.toHaveBeenCalled();

    await handlers.get(COMMAND_IDS.planStepAdd)!({ title: 'X' });
    expect(state.setPlans).not.toHaveBeenCalled();
  });
});
