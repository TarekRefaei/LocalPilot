/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';

function deprecated(): never {
  vscode.window.showErrorMessage(
    'Act v1 is deprecated and permanently disabled. Use Execute (v2).'
  );
  throw new Error('Act v1 disabled');
}

export async function startActByPlanId(): Promise<void> {
  deprecated();
}

export async function runActTask(): Promise<void> {
  deprecated();
}

export async function runAllActTasks(): Promise<void> {
  deprecated();
}

export function skipActTask(): void {
  deprecated();
}
