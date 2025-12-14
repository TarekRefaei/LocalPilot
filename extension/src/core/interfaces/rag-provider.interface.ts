import type { RetrievedChunk, ChunkType, ProjectStats } from '../entities';

/**
 * Interface for RAG operations
 */
export interface IRAGProvider {
  /** Start indexing a workspace */
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  /** Sync index (re-index only changed files) */
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  /** Query for relevant code chunks */
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  /** Get project summary after indexing */
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  /** Check if project is indexed */
  isIndexed(projectId: string): Promise<boolean>;
  /** Clear project index */
  clearIndex(projectId: string): Promise<void>;
}

export interface IndexProgress {
  phase: 'scanning' | 'parsing' | 'embedding' | 'storing';
  current: number;
  total: number;
  currentFile?: string;
  message?: string;
}

export interface IndexResult {
  success: boolean;
  filesIndexed: number;
  chunksCreated: number;
  durationSeconds: number;
  languages: string[];
  error?: string;
}

export interface SyncProgress {
  phase: 'scanning' | 'comparing' | 'updating';
  changedFiles: number;
  deletedFiles: number;
  processed: number;
  total: number;
}

export interface SyncResult {
  success: boolean;
  filesUpdated: number;
  filesDeleted: number;
  chunksUpdated: number;
  durationSeconds: number;
}

export interface QueryFilters {
  fileTypes?: string[];
  chunkTypes?: ChunkType[];
  filePaths?: string[];
}

export interface ProjectSummary {
  projectName: string;
  description: string;
  mainLanguages: string[];
  keyFiles: string[];
  architecture: string;
  frameworks: string[];
  stats: ProjectStats;
}
