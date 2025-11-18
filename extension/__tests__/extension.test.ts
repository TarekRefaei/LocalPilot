import { activate } from '@/extension';
import * as vscode from 'vscode';

type Disposable = { dispose: () => void };

describe('Extension activation', () => {
  it('registers helloWorld command and shows a message when executed', async () => {
    const context = { subscriptions: [] as Disposable[] } as any;

    activate(context);

    const registry = (vscode.commands as any).__getRegistered?.();
    expect(registry).toBeDefined();
    const handler = registry['localpilot.helloWorld'];
    expect(typeof handler).toBe('function');

    await handler();
    expect(vscode.window.showInformationMessage).toHaveBeenCalledWith('LocalPilot ready');
  });
});
