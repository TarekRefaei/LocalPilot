from typing import List, Dict


class PromptBuilder:
    """
    Phase 1.2
    ----------
    Builds a chat prompt with injected RAG context.
    No planning, no execution, no file writes.
    """

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant answering questions about a codebase.\n"
        "You must base your answers ONLY on the provided code context.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Do NOT suggest code changes or plans."
    )

    def build(
        self,
        user_message: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]

        if chunks:
            context_blocks = []
            for c in chunks:
                meta = c.get("metadata", {})
                context_blocks.append(
                    f"File: {meta.get('file_path')} "
                    f"(lines {meta.get('start_line')}–{meta.get('end_line')})\n"
                    f"```{meta.get('language', '')}\n"
                    f"{c.get('content')}\n```"
                )

            messages.append({
                "role": "system",
                "content": "CODE CONTEXT:\n\n" + "\n\n".join(context_blocks)
            })

        messages.append({"role": "user", "content": user_message})
        return messages
