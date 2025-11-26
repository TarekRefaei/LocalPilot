describe('WebSocketClient additional branches', () => {
  beforeEach(async () => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('parse invalid without error listeners does not emit', async () => {
    const { WebSocketClient } = await import('@/services/ws-client');
    const client: any = new WebSocketClient('ws://example');
    // Do NOT add error listener to hit handleError no-listener branch
    const res = client.parseMessage ? client.parseMessage('nope') : client['parseMessage']('nope');
    expect(res).toBeNull();
  });

  it('routeMessage with no subscribers is a no-op', async () => {
    const { WebSocketClient } = await import('@/services/ws-client');
    const { createEnvelope } = await import('@/contracts/envelope');
    const client: any = new WebSocketClient('ws://example');
    const env = createEnvelope('no.subscribers', {});
    // Should not throw
    if (client.routeMessage) client.routeMessage(env);
    else client['routeMessage'](env);
  });

  it('send throws when not connected', async () => {
    const { WebSocketClient } = await import('@/services/ws-client');
    const client = new WebSocketClient('ws://example');
    expect(() => client.send('topic', { a: 1 })).toThrow();
  });
});
