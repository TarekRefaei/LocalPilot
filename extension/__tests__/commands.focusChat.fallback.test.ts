describe('LocalPilot Commands: focusChatInput fallback path', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('falls back to toggleAuxiliaryBar and then opens a chat candidate', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotCommands } = await import('@/commands');
    const { COMMAND_IDS } = await import('@/ids');

    // Custom behavior: first focusAuxiliaryBar rejects, toggleAuxiliaryBar resolves,
    // and the first chat candidate resolves to mark opened=true.
    (vscode.commands.executeCommand as any).mockImplementation((cmd: string, ..._args: any[]) => {
      if (cmd === 'workbench.action.focusAuxiliaryBar') {
        return Promise.reject(new Error('no focus'));
      }
      if (cmd === 'workbench.action.toggleAuxiliaryBar') {
        return Promise.resolve(undefined);
      }
      if (cmd === 'workbench.action.chat.open') {
        return Promise.resolve(undefined);
      }
      // Default: resolve to avoid noise
      return Promise.resolve(undefined);
    });

    const context = { subscriptions: [] as any[] } as any;
    registerLocalPilotCommands(context, undefined as any);
    const calls = (vscode.commands.registerCommand as any).mock.calls as [string, Function][];
    const handler = new Map<string, Function>(calls.map(([id, fn]) => [id, fn]));

    await handler.get(COMMAND_IDS.focusChatInput)!();

    // Should have attempted fallback path and ultimately show info message for success
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith(
      'Focus Chat input (LocalPilot)',
    );
  });
});
