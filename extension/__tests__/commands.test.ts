describe('LocalPilot Commands registration', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('registers core commands and executes side effects', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS, VIEW_CONTAINER_ID } = await import('@/ids');

    type Disposable = { dispose: () => void };
    const context = { subscriptions: [] as Disposable[] } as any;
    registerLocalPilotCommands(context);

    const expected = [
      COMMAND_IDS.showViews,
      COMMAND_IDS.focusChatInput,
      COMMAND_IDS.chatTransferToPlan,
      COMMAND_IDS.planCreate,
      COMMAND_IDS.planUpdate,
      COMMAND_IDS.planDelete,
      COMMAND_IDS.actDryRun,
      COMMAND_IDS.actApprove,
      COMMAND_IDS.actApply,
      COMMAND_IDS.actRollback,
      COMMAND_IDS.indexStart,
      COMMAND_IDS.indexStop,
      COMMAND_IDS.modelSwap,
    ];

    const regCalls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handlers = new Map<string, Function>(regCalls.map(([id, fn]) => [id, fn]));

    for (const id of expected) {
      expect(handlers.has(id)).toBe(true);
    }

    await handlers.get(COMMAND_IDS.showViews)!();
    expect(vscode.commands.executeCommand).toHaveBeenCalledWith('setContext', 'localpilot.views.visible', true);
    expect(vscode.commands.executeCommand).toHaveBeenCalledWith(`workbench.view.extension.${VIEW_CONTAINER_ID}`);
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith('LocalPilot views opened');

    await handlers.get(COMMAND_IDS.indexStart)!();
    expect(vscode.commands.executeCommand).toHaveBeenCalledWith('setContext', 'localpilot.indexing.running', true);
    await handlers.get(COMMAND_IDS.indexStop)!();
    expect(vscode.commands.executeCommand).toHaveBeenCalledWith('setContext', 'localpilot.indexing.running', false);

    // Execute remaining for coverage
    await handlers.get(COMMAND_IDS.focusChatInput)!();
    await handlers.get(COMMAND_IDS.chatTransferToPlan)!();
    await handlers.get(COMMAND_IDS.planCreate)!();
    await handlers.get(COMMAND_IDS.planUpdate)!();
    await handlers.get(COMMAND_IDS.planDelete)!();
    await handlers.get(COMMAND_IDS.actDryRun)!();
    await handlers.get(COMMAND_IDS.actApprove)!();
    await handlers.get(COMMAND_IDS.actApply)!();
    await handlers.get(COMMAND_IDS.actRollback)!();
    await handlers.get(COMMAND_IDS.modelSwap)!();
  });
});
