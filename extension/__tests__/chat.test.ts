/// <reference types="jest" />
describe('Chat handler streaming and button dispatch', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('streams markdown and renders a Transfer to Plan button', async () => {
    const { createChatHandler } = await import('../src/chat');

    const handler = createChatHandler({
      onDidChange: (() => ({ dispose() {} })) as any,
      getPlans: () => [],
      getIndexingRunning: () => false,
      getRecentPrompts: () => [],
      setPlans: () => {},
      setIndexingRunning: () => {},
      setRecentPrompts: () => {},
    } as any);

    const stream = {
      progress: jest.fn(),
      markdown: jest.fn(),
      button: jest.fn(),
    } as any;

    const token = {
      onCancellationRequested: jest.fn(() => ({ dispose() {} })),
    } as any;

    await handler({ prompt: 'Implement feature X' } as any, {} as any, stream, token);

    expect(stream.markdown).toHaveBeenCalled();
    expect(stream.button).toHaveBeenCalled();

    const buttonArg = (stream.button as any).mock.calls[0][0];
    expect(buttonArg.command).toBe('localpilot.chat.transferToPlan');
    expect(Array.isArray(buttonArg.arguments)).toBe(true);
    expect(buttonArg.arguments[0]).toHaveProperty('title');
  });
});
