from typing import List, Dict
from server.prompts.chat import CHAT_SYSTEM_PROMPT


class PromptBuilder:
    """
    Phase 1.2
    ----------
    Builds a chat prompt with injected RAG context.
    No planning, no execution, no file writes.
    """

    def build(
        self,
        user_message: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        messages = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT}
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
