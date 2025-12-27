import * as fs from 'fs';
import * as path from 'path';

export class BackupManager {
  private baseDir: string;

  constructor(private readonly workspaceRoot: string) {
    this.baseDir = path.join(workspaceRoot, '.localpilot', 'backups');
    fs.mkdirSync(this.baseDir, { recursive: true });
  }

  backup(filePath: string): string | null {
    if (!fs.existsSync(filePath)) return null;

    const ts = Date.now().toString();
    const name = path.basename(filePath) + '.' + ts + '.bak';
    const dest = path.join(this.baseDir, name);

    fs.copyFileSync(filePath, dest);
    return dest;
  }

  restore(backupPath: string, targetPath: string) {
    fs.copyFileSync(backupPath, targetPath);
  }
}
