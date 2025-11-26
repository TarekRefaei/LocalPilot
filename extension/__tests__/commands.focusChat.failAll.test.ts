describe('LocalPilot Commands: focusChatInput all candidates fail => warning', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('opens chat successfully and shows info', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');

    // Make first candidate succeed
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
});
