/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';

export async function triggerIndexSync(projectId: string) {
  const ws = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
  const url = `http://127.0.0.1:8000/api/index/${encodeURIComponent(projectId)}?workspace_root=${encodeURIComponent(ws)}`;
  try {
    await fetch(url);
    vscode.window.showInformationMessage('Index updated for applied changes.');
  } catch (e) {
    vscode.window.showWarningMessage('Index sync failed. You may re-index manually.');
  }
}

