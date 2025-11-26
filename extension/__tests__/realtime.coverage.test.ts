describe('realtime service coverage helpers', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('acts resolve in test env and startIndexing handles no workspace', async () => {
    const vscode = (await import('vscode')) as any;
    // Simulate no workspace folders
    (vscode as any).workspace = { workspaceFolders: undefined };

    const { actDryRun, actApprove, actApply, actRollback, startIndexing } = await import(
      '@/services/realtime'
    );

    await expect(actDryRun({ foo: 'bar' })).resolves.toBeUndefined();
    await expect(actApprove({ id: 1 })).resolves.toBeUndefined();
    await expect(actApply({ id: 1 })).resolves.toBeUndefined();
    await expect(actRollback({ id: 1 })).resolves.toBeUndefined();

    await expect(startIndexing(undefined as any)).resolves.toBeUndefined();
  });
});
