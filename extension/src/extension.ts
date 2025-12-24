import * as vscode from 'vscode';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById } from './features/plan/plan-controller';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  const planViewProvider = new PlanViewProvider();
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
      new ActViewProvider()
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
    vscode.commands.registerCommand('localpilot.plan.regenerateById', (planId: string) => regeneratePlanById(planId, ChatSessionStore.getMessages()))
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
}

export function deactivate() {}
