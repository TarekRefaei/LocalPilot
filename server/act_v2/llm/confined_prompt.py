import json
from typing import Dict, List


SYSTEM_PROMPT = """
You are operating in EXECUTION MODE.

You MUST output a VALID unified diff.

GENERAL RULES:
- Execute EXACTLY ONE task.
- Modify ONLY the allowed files.
- Output MUST be a unified diff.
- Do NOT explain anything.
- Do NOT output markdown.
- Do NOT include JSON.

CREATE TASK RULES:
- For create actions, you MUST use:
  --- /dev/null
  +++ b/<file_path>

MODIFY TASK RULES:
- For modify actions, the file MUST already exist.
- NEVER use /dev/null for existing files.

DELETE TASK RULES:
- For delete actions, you MUST use:
  --- a/<file_path>
  +++ /dev/null

EMPTY RESULT RULE:
- If no changes are required, output an EMPTY diff.

Failure to follow ANY rule is a critical error.
""".strip()


def build_confined_prompt(context: Dict) -> List[Dict]:
    """
    Returns a sealed message list for the LLM.
    """

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": json.dumps(context, indent=2),
        },
    ]
