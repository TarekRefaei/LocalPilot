import * as vscode from 'vscode';
import {
  PLAN_REFRESH,
  PLAN_SELECT,
  PLAN_OPEN,
  PLAN_VALIDATE_BY_ID,
  PLAN_APPROVE_BY_ID,
  PLAN_DISCARD_BY_ID,
  PLAN_REGENERATE_BY_ID,
  PLAN_FIX_BY_ID,
  CHAT_CLEAR,
  ACT_START,
  ACT_FOCUS,
  ACT_REFRESH,
  ACT_RUN_TASK,
  ACT_SKIP_TASK,
  ACT_RUN_ALL,
  INDEX_SYNC,
  EXECUTE_START,
  EXECUTE_APPLY,
  EXECUTE_RESUME,
  EXECUTE_SKIP,
  EXECUTE_RETRY,
  EXECUTE_REFRESH,
  WORKBENCH_FOCUS_LOCALPILOT,
} from './config/commands.config';
import { MSG_ACTIVATED, MSG_CHAT_CLEARED, MSG_ACT_V1_DEPRECATED } from './config/messages.config';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { ExecuteViewProvider } from './views/execute/execute-view';
import { startPlanExecution, approveAndApply, refreshExecution, resumeExecutionAction, skipTaskAction, retryTaskAction } from './features/execute_v2/execute-controller';
import * as api from './features/execute_v2/execute-client';
import { executionState } from './features/execute_v2/execute-state';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById, fixPlanById } from './features/plan/plan-controller';
import { ActPersistence } from './features/act/act-persistence';
import { actState } from './features/act/act-state';

export function activate(context: vscode.ExtensionContext) {
  console.log(MSG_ACTIVATED);
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
    vscode.commands.registerCommand(PLAN_REFRESH, () => {
      const plans = getAllPlans();
      planViewProvider.update(plans);
    }),
    vscode.commands.registerCommand(PLAN_SELECT, selectPlan),
    vscode.commands.registerCommand(PLAN_OPEN, openPlan),
    vscode.commands.registerCommand(PLAN_VALIDATE_BY_ID, validatePlanById),
    vscode.commands.registerCommand(PLAN_APPROVE_BY_ID, approvePlanById),
    vscode.commands.registerCommand(PLAN_DISCARD_BY_ID, discardPlanById),
    vscode.commands.registerCommand(PLAN_REGENERATE_BY_ID, (planId: string) => regeneratePlanById(planId, ChatSessionStore.getMessages())),
    vscode.commands.registerCommand(PLAN_FIX_BY_ID, fixPlanById),
    // Removed: localpilot.plan.fixJsonById — frontend auto-mutation is disallowed
  );
  const clearChat = vscode.commands.registerCommand(CHAT_CLEAR, () => {
    ChatSessionStore.clear();
    vscode.window.showInformationMessage(MSG_CHAT_CLEARED);
  });
  context.subscriptions.push(clearChat);

  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
      ChatSessionStore.clear();
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      ACT_START,
      () => {
        vscode.window.showErrorMessage(MSG_ACT_V1_DEPRECATED);
      }
    ),
    vscode.commands.registerCommand(
      ACT_FOCUS,
      () => vscode.commands.executeCommand(WORKBENCH_FOCUS_LOCALPILOT)
    ),
    vscode.commands.registerCommand(
      ACT_REFRESH,
      () => actViewProvider.render()
    ),
    vscode.commands.registerCommand(
      ACT_RUN_TASK,
      () => vscode.window.showErrorMessage(MSG_ACT_V1_DEPRECATED)
    ),
    vscode.commands.registerCommand(
      ACT_SKIP_TASK,
      () => vscode.window.showErrorMessage(MSG_ACT_V1_DEPRECATED)
    ),
    vscode.commands.registerCommand(
      ACT_RUN_ALL,
      () => vscode.window.showErrorMessage(MSG_ACT_V1_DEPRECATED)
    ),
    vscode.commands.registerCommand(
      INDEX_SYNC,
      async () => { /* no-op placeholder */ }
    ),
    vscode.commands.registerCommand(
      EXECUTE_START,
      startPlanExecution
    ),
    vscode.commands.registerCommand(
      EXECUTE_APPLY,
      approveAndApply
    ),
    vscode.commands.registerCommand(
      EXECUTE_RESUME,
      resumeExecutionAction
    ),
    vscode.commands.registerCommand(
      EXECUTE_SKIP,
      skipTaskAction
    ),
    vscode.commands.registerCommand(
      EXECUTE_RETRY,
      retryTaskAction
    ),
    vscode.commands.registerCommand(
      EXECUTE_REFRESH,
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
