type Disposable = { dispose: () => void };

declare const jest: any;

const registry: Record<string, Function> = {};
const treeProviders: Record<string, any> = {};

export const window = {
  showInformationMessage: jest.fn(() => Promise.resolve(undefined)),
  registerTreeDataProvider: jest.fn((viewId: string, provider: any): Disposable => {
    treeProviders[viewId] = provider;
    return { dispose() {} };
  }),
  registerWebviewViewProvider: jest.fn((_viewId: string, _provider: any, _options?: any): Disposable => {
    return { dispose() {} };
  }),
};

export const commands = {
  registerCommand: jest.fn((command: string, callback: Function): Disposable => {
    registry[command] = callback;
    return { dispose() {} };
  }),
  executeCommand: jest.fn((_command: string, ..._args: any[]) => Promise.resolve(undefined)),
  __getRegistered: () => registry,
};

export const TreeItemCollapsibleState = {
  None: 0,
  Collapsed: 1,
  Expanded: 2,
} as const;

export class TreeItem {
  label?: string;
  collapsibleState?: number;
  contextValue?: string;
  iconPath?: any;
  command?: any;
  constructor(label?: string, collapsibleState?: number) {
    if (label !== undefined) this.label = label;
    if (collapsibleState !== undefined) this.collapsibleState = collapsibleState;
  }
}

export class EventEmitter<T = void> {
  private listeners: Array<(e: T) => any> = [];
  public readonly event = (listener: (e: T) => any): Disposable => {
    this.listeners.push(listener);
    return { dispose() {} };
  };
  public fire(data: T): void {
    for (const l of this.listeners) l(data);
  }
  public dispose(): void {
    this.listeners = [];
  }
}

export const Uri = {
  joinPath: (..._args: any[]) => ({})
} as any;

export const chat = {
  createChatParticipant: jest.fn((_id: string, _handler: Function) => ({
    iconPath: undefined,
    dispose() {}
  })),
};
