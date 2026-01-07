/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';
import { OllamaChatClient, type ChatMessage } from '../../ollama/ollama-chat-client.js';
import { ACT_MODE_SYSTEM_PROMPT } from '../../prompts/act_v1/act.prompt.js';
import type { Task } from '../../core/entities/task.entity';

export async function executeTask(
  task: Task,
  workspaceRoot: vscode.Uri
): Promise<string> {
  const client = new OllamaChatClient();

  const messages: ChatMessage[] = [
    { role: 'system', content: ACT_MODE_SYSTEM_PROMPT },
    {
      role: 'user',
      content: JSON.stringify({
        task: {
          id: task.id,
          title: task.title,
          filePath: task.filePath,
          actionType: task.actionType,
          details: task.details,
        },
        workspaceRoot: workspaceRoot.fsPath,
      }),
    },
  ];

  return client.chat(messages);
}

