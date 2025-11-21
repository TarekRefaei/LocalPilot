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
    const linkType: fs.symlink.Type = process.platform === 'win32' ? 'junction' : 'dir';
    try {
      fs.symlinkSync(realDevPath, linkPath, linkType);
    } catch (err) {
      // Fall back to copy if symlink/junction is not permitted
      const copyDir = (src: string, dest: string) => {
        fs.mkdirSync(dest, { recursive: true });
        for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
          const s = path.join(src, entry.name);
          const d = path.join(dest, entry.name);
          if (entry.isDirectory()) {
            copyDir(s, d);
          } else if (entry.isFile()) {
            fs.copyFileSync(s, d);
          }
        }
      };
      copyDir(realDevPath, linkPath);
    }
    // Allow filesystem to settle
    await new Promise((r) => setTimeout(r, 100));

    const extensionDevelopmentPath = linkPath;
    const extensionTestsPath = path.join(linkPath, 'out', 'test', 'suite', 'index');

    const version = process.env.VSCODE_TEST_VERSION || '1.106.2';
    const vscodeExecutablePath = process.env.VSCODE_TEST_EXE;
    const vscodeExecutableDir = process.env.VSCODE_TEST_DIR;
    const options: Parameters<typeof runTests>[0] = {
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: ['--disable-extensions'],
    };
    const candidatePaths: string[] = [];
    if (vscodeExecutablePath) {
      candidatePaths.push(vscodeExecutablePath);
    }
    if (vscodeExecutableDir) {
      candidatePaths.push(path.join(vscodeExecutableDir, 'Code.exe'));
    }
    // Reuse cached download under repo if present
    const archiveDirName = `vscode-win32-x64-archive-${version}`;
    candidatePaths.push(path.join(realDevPath, '.vscode-test', archiveDirName, 'Code.exe'));
    candidatePaths.push(path.join(linkPath, '.vscode-test', archiveDirName, 'Code.exe'));

    for (const p of candidatePaths) {
      try {
        if (p && fs.existsSync(p)) {
          (options as any).vscodeExecutablePath = p;
          break;
        }
      } catch {}
    }

    await runTests(options);
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('Failed to run integration tests', err);
    process.exit(1);
  }
}

main();
