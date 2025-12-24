import * as vscode from 'vscode';
import { createPlanFromChat, validateCurrentPlan, approveCurrentPlan, discardCurrentPlan, regeneratePlan } from '../features/plan/plan-controller';
import { ChatSessionStore } from '../features/chat/chat-session.store';

export function registerPlanCommands(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand(
      'localpilot.plan.createFromChat',
      async () => {
        const chatMessages = ChatSessionStore.getMessages();
        if (!chatMessages || chatMessages.length === 0) {
          vscode.window.showWarningMessage('No chat history available to generate a plan.');
          return;
        }
        await createPlanFromChat(chatMessages);
      }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.validate',
      async () => { await validateCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.approve',
      async () => { await approveCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.discard',
      async () => { await discardCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.regenerate',
      async () => { await regeneratePlan(ChatSessionStore.getMessages()); }
    )
  );
}
