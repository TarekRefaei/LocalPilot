const assert = require('assert');
const vscode = require('vscode');

describe('Extension Test Suite', () => {
  it('Open custom LocalPilot webview', async () => {
    await vscode.commands.executeCommand('localpilot.openWebview');
    assert.ok(true);
  });
});
