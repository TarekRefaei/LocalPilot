/// <reference types="jest" />

describe('MementoState migration from legacy plans', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('migrates legacy {id,title} array to Plan v2', async () => {
    const { MementoState } = await import('@/services/state');

    const legacy = [
      { id: '1', title: 'Legacy Plan 1' },
      { id: '2', title: 'Legacy Plan 2' },
    ];

    const store: Map<string, any> = new Map();
    store.set('localpilot.plans', legacy);

    const memento = {
      get: (k: string) => store.get(k),
      update: (k: string, v: any) => {
        store.set(k, v);
        return Promise.resolve();
      },
    } as any;

    const state = new MementoState(memento);
    const plans = state.getPlans();

    expect(plans.length).toBe(2);
    expect(plans[0]).toHaveProperty('version', 2);
    expect(plans[0]).toHaveProperty('steps');
    expect(plans[0]).toHaveProperty('acceptance');
    expect(typeof (plans[0] as any).createdAt).toBe('string');

    // Verify persistence updates for setters
    const beforePlans = store.get('localpilot.plans');
    state.setPlans([...plans] as any);
    const afterPlans = store.get('localpilot.plans');
    expect(afterPlans).not.toBe(beforePlans);

    state.setIndexingRunning(true);
    expect(store.get('localpilot.indexing')).toBe(true);

    state.setRecentPrompts(['x']);
    expect(store.get('localpilot.recentPrompts')).toEqual(['x']);
  });
});
