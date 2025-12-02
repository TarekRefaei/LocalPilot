const assert = require('assert');
const vscode = require('vscode');

suite('Extension Test Suite', () => {
  test('Open custom LocalPilot webview', async () => {
    await vscode.commands.executeCommand('localpilot.openWebview');
    assert.strictEqual(true, true);
  });
});
