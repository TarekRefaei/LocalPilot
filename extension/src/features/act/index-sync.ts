import * as vscode from 'vscode';

export async function triggerIndexSync(projectId: string) {
  const url = `http://127.0.0.1:8000/api/index/${encodeURIComponent(projectId)}`;
  try {
    await fetch(url);
    vscode.window.showInformationMessage('Index updated for applied changes.');
  } catch (e) {
    vscode.window.showWarningMessage('Index sync failed. You may re-index manually.');
  }
}
