describe('Act Mode settings schema (package.json)', () => {
  it('exposes Act settings with correct defaults and types', () => {
    const pkg = require('../package.json');
    const props = pkg?.contributes?.configuration?.properties || {};

    // Apply safety mode
    expect(props['localpilot.act.applySafety']).toBeDefined();
    expect(props['localpilot.act.applySafety'].type).toBe('string');
    expect(Array.isArray(props['localpilot.act.applySafety'].enum)).toBe(true);
    expect(props['localpilot.act.applySafety'].default).toBe('strict');

    // Auto-approve rules
    expect(props['localpilot.act.autoApprove.safeCreates']).toBeDefined();
    expect(props['localpilot.act.autoApprove.safeCreates'].type).toBe('boolean');
    expect(props['localpilot.act.autoApprove.safeCreates'].default).toBe(true);

    expect(props['localpilot.act.autoApprove.configFiles']).toBeDefined();
    expect(props['localpilot.act.autoApprove.configFiles'].type).toBe('boolean');
    expect(props['localpilot.act.autoApprove.configFiles'].default).toBe(false);

    // Approval timeout
    expect(props['localpilot.act.approvalTimeoutSeconds']).toBeDefined();
    expect(['number','integer']).toContain(props['localpilot.act.approvalTimeoutSeconds'].type);
    expect(props['localpilot.act.approvalTimeoutSeconds'].default).toBe(300);
  });
});
