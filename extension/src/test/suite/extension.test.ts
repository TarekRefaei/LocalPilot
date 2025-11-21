import * as assert from 'assert';
import * as vscode from 'vscode';

// Detect if running in CI environment
// GitHub Actions sets CI=true, but also check common CI env vars
const isInCI = !!(
  process.env.CI ||
  process.env.CONTINUOUS_INTEGRATION ||
  process.env.GITHUB_ACTIONS ||
  process.env.GITLAB_CI ||
  process.env.CIRCLECI
);
const isCiLinux = process.platform === 'linux' && isInCI;

suite('LocalPilot Integration', () => {
  test('registers core commands', async () => {
    const ext = vscode.extensions.getExtension('tarekrefaei.localpilot');
    assert.ok(ext, 'Extension not found');
    await ext.activate();
    const cmds = await vscode.commands.getCommands(true);
    const needed = [
      'localpilot.helloWorld',
      'localpilot.showViews',
      'localpilot.focusChatInput',
      'localpilot.chat.transferToPlan',
      'localpilot.plan.create',
      'localpilot.plan.update',
      'localpilot.plan.delete',
      'localpilot.act.dryRun',
      'localpilot.act.approve',
      'localpilot.act.apply',
      'localpilot.act.rollback',
      'localpilot.index.start',
      'localpilot.index.stop',
      'localpilot.model.swap',
    ];
    for (const c of needed) {
      assert.ok(cmds.includes(c), `Command missing: ${c}`);
    }
  });

  (isCiLinux ? test.skip : test)('can focus LocalPilot view container', async () => {
    await vscode.commands.executeCommand('workbench.view.extension.localpilot');
  });

  // See CI-only skip below for this state mutation test

  (isCiLinux ? test.skip : test)('Transfer to Plan command inserts a draft into state', async () => {
    const ext = vscode.extensions.getExtension('tarekrefaei.localpilot');
    assert.ok(ext, 'Extension not found');
    const api: any = await ext.activate();
    const before = api.state.getPlans();
    await vscode.commands.executeCommand('localpilot.chat.transferToPlan', { title: 'Demo Plan' });
    const after = api.state.getPlans();
    assert.ok(after.length === before.length + 1, 'Plan was not inserted');
    assert.ok(after.some((p: any) => p.title === 'Demo Plan'));
  });

  // This test requires a running backend with WebSocket support
  // Skip it on CI since we don't have a backend service running
  (isInCI ? test.skip : test)('Indexing start/stop commands synchronize state', async function () {
    this.timeout(10000);
    const ext = vscode.extensions.getExtension('tarekrefaei.localpilot');
    assert.ok(ext, 'Extension not found');
    const api: any = await ext.activate();
    await vscode.commands.executeCommand('localpilot.index.start');
    assert.strictEqual(api.state.getIndexingRunning(), true);
    await vscode.commands.executeCommand('localpilot.index.stop');
    assert.strictEqual(api.state.getIndexingRunning(), false);
  });
});
