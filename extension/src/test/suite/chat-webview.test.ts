import * as assert from 'assert';
import * as vscode from 'vscode';

const isCiLinux = process.platform === 'linux' && !!process.env.CI;

const maybeSuite = isCiLinux ? suite.skip : suite;

maybeSuite('Chat Webview Integration', () => {
  test('chat provider test command returns computed state', async () => {
    const ext = vscode.extensions.getExtension('tarekrefaei.localpilot');
    assert.ok(ext, 'Extension not found');
    const api: any = await ext.activate();

    const cmds = await vscode.commands.getCommands(true);
    assert.ok(
      cmds.includes('localpilot.__test.chat.computeState'),
      'computeState test command is not registered'
    );

    // Mutate state and config, then verify computeState reflects it
    const beforeModel = String(vscode.workspace.getConfiguration('localpilot').get('model') ?? 'local');

    try {
      api.state.setPlans([{ id: 'p1', title: 'Plan A' }]);
      api.state.setRecentPrompts(['Build chat webview']);
      await vscode.workspace
        .getConfiguration('localpilot')
        .update('model', 'openai:gpt-4o-mini', vscode.ConfigurationTarget.Global);

      const s: any = await vscode.commands.executeCommand('localpilot.__test.chat.computeState');
      assert.ok(s, 'No state returned');
      assert.strictEqual(s.plans, 1);
      assert.ok(Array.isArray(s.recent));
      assert.strictEqual(s.recent[0], 'Build chat webview');
      assert.strictEqual(s.model, 'openai:gpt-4o-mini');
    } finally {
      await vscode.workspace
        .getConfiguration('localpilot')
        .update('model', beforeModel, vscode.ConfigurationTarget.Global);
    }
  });
});
