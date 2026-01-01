/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as fs from 'fs';
import * as path from 'path';

export class FileWriter {
  write(filePath: string, content: string) {
    const dir = path.dirname(filePath);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(filePath, content, 'utf-8');
  }

  delete(filePath: string) {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
}

