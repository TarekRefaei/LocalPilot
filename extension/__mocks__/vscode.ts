type Disposable = { dispose: () => void };

const registry: Record<string, Function> = {};

export const window = {
  showInformationMessage: jest.fn(() => Promise.resolve(undefined)),
};

export const commands = {
  registerCommand: jest.fn((command: string, callback: Function): Disposable => {
    registry[command] = callback;
    return { dispose() {} };
  }),
  __getRegistered: () => registry,
};
