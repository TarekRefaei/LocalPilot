import * as vscode from 'vscode';
import * as path from 'path';

/**
 * VERY SMALL unified diff applier.
 * Supports add/replace lines.
 * (Enough for Phase 4.8; full patch engine can come later.)
 */
export async function applyDiff(diff: string): Promise<boolean> {
  if (!diff.trim().startsWith('---')) {
    // empty or invalid diff = no-op success
    return true;
  }

  const lines = diff.split('\n');

  let targetFile: string | null = null;
  const hunks: string[] = [];

  for (const line of lines) {
    if (line.startsWith('+++ ')) {
      targetFile = line.replace('+++ ', '').trim();
      continue;
    }
    if (targetFile) hunks.push(line);
  }

  if (!targetFile) {
    vscode.window.showErrorMessage('Invalid diff: no target file.');
    return false;
  }

  const ws = vscode.workspace.workspaceFolders?.[0];
  if (!ws) {
    vscode.window.showErrorMessage('No workspace open.');
    return false;
  }

  const filePath = vscode.Uri.file(
    path.join(ws.uri.fsPath, targetFile.replace(/^b\//, ''))
  );

  const doc = await vscode.workspace.openTextDocument(filePath);
  const text = doc.getText();
  const newText = applyUnifiedDiff(text, hunks);

  if (newText === null) {
    vscode.window.showErrorMessage('Failed to apply diff.');
    return false;
  }

  const edit = new vscode.WorkspaceEdit();
  edit.replace(
    filePath,
    new vscode.Range(
      doc.positionAt(0),
      doc.positionAt(text.length)
    ),
    newText
  );

  return vscode.workspace.applyEdit(edit);
}

/**
 * VERY BASIC unified diff applier.
 * (Insert/remove lines only; safe for generated code.)
 */
function applyUnifiedDiff(original: string, diffLines: string[]): string | null {
  const out: string[] = [];
  const src = original.split('\n');
  let srcIndex = 0;

  for (const line of diffLines) {
    if (line.startsWith('@@')) continue;

    if (line.startsWith('+')) {
      out.push(line.slice(1));
    } else if (line.startsWith('-')) {
      srcIndex++;
    } else {
      out.push(src[srcIndex] ?? '');
      srcIndex++;
    }
  }

  return out.join('\n');
}
