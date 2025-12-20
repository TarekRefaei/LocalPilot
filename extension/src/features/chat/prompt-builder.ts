export class PromptBuilder {
  private static SYSTEM_PROMPT = (
    "You are a helpful AI assistant answering questions about a codebase.\n" +
    "You must base your answers ONLY on the provided context.\n" +
    "If the answer is not in the context, say \"I don't know\".\n" +
    "Do NOT suggest code changes or plans."
  );

  build(userMessage: string, chunks: any[]): Array<{ role: string; content: string }> {
    const messages: Array<{ role: string; content: string }> = [
      { role: "system", content: PromptBuilder.SYSTEM_PROMPT }
    ];

    if (chunks && chunks.length > 0) {
      const blocks = chunks.map((c: any) => {
        const m = c.metadata || {};
        const lang = m.language || "";
        const file = m.file_path || "";
        const start = m.start_line ?? "";
        const end = m.end_line ?? "";
        const content = c.content ?? "";
        return `File: ${file} (lines ${start}–${end})\n\u0060\u0060\u0060${lang}\n${content}\n\u0060\u0060\u0060`;
      });

      messages.push({
        role: "system",
        content: "CODE CONTEXT:\n\n" + blocks.join("\n\n")
      });
    }

    messages.push({ role: "user", content: userMessage });
    return messages;
  }
}
