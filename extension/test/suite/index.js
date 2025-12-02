const assert = require('assert');
const vscode = require('vscode');
const { describe, it } = require('mocha');

describe('Extension Test Suite', () => {
  it('Open custom LocalPilot webview', async () => {
    await vscode.commands.executeCommand('localpilot.openWebview');
    assert.ok(true);
  });
});
