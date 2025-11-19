import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import { runTests } from '@vscode/test-electron';

async function main() {
  try {
    const realDevPath = path.resolve(__dirname, '../..');
    const tmpRoot = path.join(os.tmpdir(), 'localpilot-e2e');
    const linkPath = path.join(tmpRoot, 'ext');
    // Ensure temp root
    fs.mkdirSync(tmpRoot, { recursive: true });
    // Recreate junction to a path without spaces
    try {
      fs.rmSync(linkPath, { recursive: true, force: true });
    } catch {}
    fs.symlinkSync(realDevPath, linkPath, 'junction');

    const extensionDevelopmentPath = linkPath;
    const extensionTestsPath = path.join(linkPath, 'out', 'test', 'suite', 'index');

    await runTests({
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: ['--disable-extensions']
    });
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('Failed to run integration tests', err);
    process.exit(1);
  }
}

main();
