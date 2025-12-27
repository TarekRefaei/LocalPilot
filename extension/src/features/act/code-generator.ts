import { ACT_SYSTEM_PROMPT, buildActPrompt } from './act-prompts';

type GenerateArgs = {
  model: string;
  actionType: 'create' | 'modify' | 'delete';
  filePath: string;
  taskTitle: string;
  taskDescription: string;
  details: string[];
  existingContent?: string;
  ragContext?: string;
};

export class CodeGenerator {
  constructor(private readonly baseUrl = 'http://127.0.0.1:11434') {}

  async generate(args: GenerateArgs): Promise<string> {
    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: args.model,
        messages: [
          { role: 'system', content: ACT_SYSTEM_PROMPT },
          { role: 'user', content: buildActPrompt(args) }
        ],
        stream: false,
        options: { temperature: 0 }
      })
    });

    if (!res.ok) {
      throw new Error(`LLM generation failed: ${res.status}`);
    }

    const data = await res.json();
    const content = (data?.message?.content ?? '').trim();

    if (!content) {
      throw new Error('Empty code generation output.');
    }

    return content;
  }
}
