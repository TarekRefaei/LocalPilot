import * as vscode from 'vscode';
import { COMMAND_IDS } from './ids';
import type { LocalPilotState } from './services/state';

export function createChatHandler(state: LocalPilotState): vscode.ChatRequestHandler {
  return (request, _context, stream, token) => {
    const prompt = request.prompt ?? '';
    const planCount = state.getPlans().length;

    const sub = token.onCancellationRequested(() => {
      stream.progress('Cancelled');
    });

    try {
      stream.progress('Preparing response...');
      // Simple streamed markdown response
      stream.markdown('### LocalPilot\n');
      stream.markdown('I can draft a plan from your request.\n\n');
      stream.markdown(`You currently have ${planCount} plan(s).\n`);
      stream.markdown('Preview:');
      const title = `Draft plan: ${prompt.slice(0, 40) || 'Untitled'}`;
      stream.markdown(`\n- ${title}\n`);

      // Provide an action to transfer this draft into Plans
      stream.button({
        command: COMMAND_IDS.chatTransferToPlan,
        title: 'Transfer to Plan',
        arguments: [{ title, prompt }],
      });
    } finally {
      sub?.dispose?.();
    }
    // ChatResult optional
  };
}

export function registerLocalPilotChat(
  context: vscode.ExtensionContext,
  state: LocalPilotState
): void {
  const handler = createChatHandler(state);
  const participant = vscode.chat.createChatParticipant('localpilot', handler);
  context.subscriptions.push(participant);
}
