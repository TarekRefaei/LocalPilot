/**
 * Represents an indexed project/workspace
 */
export interface Project {
  /** Unique identifier (hash of workspace path) */
  id: string;
  /** Display name (folder name) */
  name: string;
  /** Absolute path to workspace */
  workspacePath: string;
  /** Index status */
  indexStatus: IndexStatus;
  /** When indexing was last completed */
  lastIndexedAt: Date | null;
  /** Statistics about indexed content */
  stats: ProjectStats;
  /** Languages detected in project */
  languages: string[];
}

export type IndexStatus =
  | 'not-indexed'
  | 'indexing'
  | 'indexed'
  | 'sync-required'
  | 'error';

export interface ProjectStats {
  filesCount: number;
  chunksCount: number;
  totalLines: number;
  byLanguage: Record<string, number>;
}
