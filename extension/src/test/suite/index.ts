import * as path from 'path';
import * as fs from 'fs';
import Mocha from 'mocha';

export function run(): Promise<void> {
  const mocha = new Mocha({
    ui: 'tdd',
    color: true,
    timeout: 20000,
  });

  const testsRoot = path.resolve(__dirname, '.');

  function walk(dir: string, acc: string[]): string[] {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(p, acc);
      } else if (entry.isFile() && p.endsWith('.test.js')) {
        acc.push(p);
      }
    }
    return acc;
  }

  return new Promise((resolve, reject) => {
    try {
      const files = walk(testsRoot, []);
      for (const f of files) {
        mocha.addFile(path.resolve(testsRoot, f));
      }
      mocha.run((failures: number) => {
        if (failures > 0) {
          reject(new Error(`${failures} tests failed.`));
        } else {
          resolve();
        }
      });
    } catch (err: unknown) {
      if (err instanceof Error) {
        reject(err);
      } else {
        reject(new Error(String(err)));
      }
    }
  });
}
