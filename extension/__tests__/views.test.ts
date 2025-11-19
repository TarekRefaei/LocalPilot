describe('LocalPilot Views registration', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('registers four TreeDataProviders for Plans/Act/Indexing/Status', async () => {
    const vscode = (await import('vscode')) as typeof import('vscode');
    const { registerLocalPilotViews } = await import('@/views/register');
    const { VIEW_IDS } = await import('@/ids');

    type Disposable = { dispose: () => void };
    const context = { subscriptions: [] as Disposable[] } as any;
    registerLocalPilotViews(context);

    const calls = (vscode.window.registerTreeDataProvider as any).mock.calls as [string, any][];
    expect(calls.length).toBe(4);

    const viewIds = new Set(calls.map((c) => c[0]));
    expect(viewIds.has(VIEW_IDS.plans)).toBe(true);
    expect(viewIds.has(VIEW_IDS.act)).toBe(true);
    expect(viewIds.has(VIEW_IDS.indexing)).toBe(true);
    expect(viewIds.has(VIEW_IDS.status)).toBe(true);

    // Ensure each provider returns at least one item
    for (const [, provider] of calls) {
      const children = await provider.getChildren();
      expect(Array.isArray(children)).toBe(true);
      expect(children.length).toBeGreaterThan(0);
      for (const item of children) {
        expect(item).toBeInstanceOf(vscode.TreeItem as any);
      }
    }
  });
});
