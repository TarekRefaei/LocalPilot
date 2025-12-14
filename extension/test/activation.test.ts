import { describe, it, expect, vi } from 'vitest';

vi.mock('vscode', () => {
  return {
    window: {
      registerWebviewViewProvider: vi.fn(() => ({ dispose: vi.fn() })),
    },
  };
});

import { activate } from '../src/extension';

describe('Extension activation', () => {
  it('should activate without throwing and register the panel', () => {
    const subscriptions: { dispose?: () => void }[] = [];
    const context = { subscriptions } as any;

    expect(() => activate(context)).not.toThrow();
    expect(subscriptions.length).toBeGreaterThan(0);
  });
});
