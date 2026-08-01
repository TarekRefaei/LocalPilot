export interface WorkspaceSnapshot {
  /** Absolute workspace root path */
  rootPath: string;

  /** Set of workspace-relative file paths that currently exist */
  existingFiles: Set<string>;

  /** Set of workspace-relative file paths that are indexed (advisory) */
  indexedFiles: Set<string>;
}
