/**
 * Interface for file system operations
 */
export interface IFileSystem {
  /** Read file content */
  readFile(filePath: string): Promise<string>;
  /** Write content to file (creates if not exists) */
  writeFile(filePath: string, content: string): Promise<void>;
  /** Delete a file */
  deleteFile(filePath: string): Promise<void>;
  /** Check if file exists */
  exists(filePath: string): Promise<boolean>;
  /** Create directory (recursive) */
  createDirectory(dirPath: string): Promise<void>;
  /** List files in directory */
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  /** Get file stats */
  stat(filePath: string): Promise<FileStat>;
  /** Create backup of a file */
  backup(filePath: string): Promise<string>;
  /** Restore file from backup */
  restore(backupPath: string, targetPath: string): Promise<void>;
  /** Get workspace root path */
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}
