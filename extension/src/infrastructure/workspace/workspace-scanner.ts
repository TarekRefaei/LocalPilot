import * as path from 'path';
import * as vscode from 'vscode';
import type { WorkspaceSnapshot } from '../../domain/workspace.snapshot';

function toWorkspaceRelativePath(rootPath: string, fileFsPath: string): string {
  const rel = path.relative(rootPath, fileFsPath);
  return rel.replace(/\\/g, '/');
}

export async function buildWorkspaceSnapshot(
  indexedFiles: string[] = []
): Promise<WorkspaceSnapshot> {
  const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
  if (!workspaceFolder) {
    throw new Error('No workspace folder is open.');
  }

  const rootPath = workspaceFolder.uri.fsPath;
  const files = await vscode.workspace.findFiles('**/*', '**/{node_modules,.git}/**');

  const existingFiles = new Set<string>();
  for (const file of files) {
    const rel = toWorkspaceRelativePath(rootPath, file.fsPath);
    existingFiles.add(rel);
  }

  return {
    rootPath,
    existingFiles,
    indexedFiles: new Set(indexedFiles),
  };
}
