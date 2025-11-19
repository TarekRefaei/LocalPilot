import * as assert from 'assert';
import * as vscode from 'vscode';

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

  test('can focus LocalPilot view container', async () => {
    await vscode.commands.executeCommand('workbench.view.extension.localpilot');
  });
});
