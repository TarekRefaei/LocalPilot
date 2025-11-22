/// <reference types="jest" />

describe('realtime.startIndexing (unit path)', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('sets context and state immediately in test env', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { startIndexing } = await import('@/services/realtime');

    const state = { setIndexingRunning: jest.fn() } as any;
    await startIndexing(state);

    expect(vscode.commands.executeCommand).toHaveBeenCalledWith('setContext', 'localpilot.indexing.running', true);
    expect(state.setIndexingRunning).toHaveBeenCalledWith(true);
  });
});
