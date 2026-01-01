import * as vscode from 'vscode';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { ExecuteViewProvider } from './views/execute/execute-view';
import { startPlanExecution, approveAndApply } from './features/execute_v2/execute-controller';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById } from './features/plan/plan-controller';
import { ActPersistence } from './features/act/act-persistence';
import { actState } from './features/act/act-state';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  const planViewProvider = new PlanViewProvider();
  const actViewProvider = new ActViewProvider();
  const executeViewProvider = new ExecuteViewProvider();
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      ChatViewProvider.viewId,
      new ChatViewProvider()
    ),
    vscode.window.registerWebviewViewProvider(
      PlanViewProvider.viewId,
      planViewProvider
    ),
    vscode.window.registerWebviewViewProvider(
      ActViewProvider.viewId,
      actViewProvider
    ),
    vscode.window.registerWebviewViewProvider(
      ExecuteViewProvider.viewId,
      executeViewProvider
    )
  );
  registerPlanCommands(context);
  context.subscriptions.push(
    vscode.commands.registerCommand('localpilot.plan.refresh', () => {
      const plans = getAllPlans();
      planViewProvider.update(plans);
    }),
    vscode.commands.registerCommand('localpilot.plan.select', selectPlan),
    vscode.commands.registerCommand('localpilot.plan.open', openPlan),
    vscode.commands.registerCommand('localpilot.plan.validateById', validatePlanById),
    vscode.commands.registerCommand('localpilot.plan.approveById', approvePlanById),
    vscode.commands.registerCommand('localpilot.plan.discardById', discardPlanById),
    vscode.commands.registerCommand('localpilot.plan.regenerateById', (planId: string) => regeneratePlanById(planId, ChatSessionStore.getMessages())),
    // Removed: localpilot.plan.fixJsonById — frontend auto-mutation is disallowed
  );
  const clearChat = vscode.commands.registerCommand('localpilot.chat.clear', () => {
    ChatSessionStore.clear();
    vscode.window.showInformationMessage('LocalPilot chat cleared.');
  });
  context.subscriptions.push(clearChat);

  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
      ChatSessionStore.clear();
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      'localpilot.act.start',
      () => {
        vscode.window.showErrorMessage('Act v1 is deprecated and disabled. Use Execute (v2).');
      }
    ),
    vscode.commands.registerCommand(
      'localpilot.act.focus',
      () => vscode.commands.executeCommand('workbench.view.extension.localpilot')
    ),
    vscode.commands.registerCommand(
      'localpilot.act.refresh',
      () => actViewProvider.render()
    ),
    vscode.commands.registerCommand(
      'localpilot.act.runTask',
      () => vscode.window.showErrorMessage('Act v1 is deprecated and disabled. Use Execute (v2).')
    ),
    vscode.commands.registerCommand(
      'localpilot.act.skipTask',
      () => vscode.window.showErrorMessage('Act v1 is deprecated and disabled. Use Execute (v2).')
    ),
    vscode.commands.registerCommand(
      'localpilot.act.runAll',
      () => vscode.window.showErrorMessage('Act v1 is deprecated and disabled. Use Execute (v2).')
    ),
    vscode.commands.registerCommand(
      'localpilot.index.sync',
      async () => { /* no-op placeholder */ }
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.start',
      startPlanExecution
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.apply',
      approveAndApply
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.refresh',
      () => executeViewProvider.render()
    )
  );

  // Act Mode: load persisted session on startup and save on deactivate
  const persistence = new ActPersistence(context);
  const restored = persistence.load();
  if (restored) {
    actState.set(restored);
  }

  context.subscriptions.push({
    dispose() {
      const s = actState.get();
      if (s) persistence.save(s);
    },
  });
}

export function deactivate() {}
