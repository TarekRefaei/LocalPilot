import * as path from 'path';

export function isAbsolutePath(fp: string): boolean {
  if (!fp) return false;
  // Windows absolute path (e.g. C:\ or D:/)
  if (/^[A-Za-z]:[\\/]/.test(fp)) return true;
  // Unix absolute path
  if (fp.startsWith('/')) return true;
  return false;
}

export function normalizeFilePath(fp: string): string {
  if (!fp) return fp;
  if (isAbsolutePath(fp)) {
    return path.basename(fp);
  }
  return fp;
}
