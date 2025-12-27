import * as vscode from 'vscode';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById, fixPlanJsonById } from './features/plan/plan-controller';
import { ActPersistence } from './features/act/act-persistence';
import { actState } from './features/act/act-state';
import { startActByPlanId, runActTask, runAllActTasks, skipActTask } from './features/act/act-controller';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  const planViewProvider = new PlanViewProvider();
  const actViewProvider = new ActViewProvider();
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
    vscode.commands.registerCommand('localpilot.plan.fixJsonById', fixPlanJsonById)
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
      startActByPlanId
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
      runActTask
    ),
    vscode.commands.registerCommand(
      'localpilot.act.skipTask',
      skipActTask
    ),
    vscode.commands.registerCommand(
      'localpilot.act.runAll',
      runAllActTasks
    ),
    vscode.commands.registerCommand(
      'localpilot.index.sync',
      async () => { /* no-op placeholder */ }
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
