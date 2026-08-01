import json
from typing import Any, Dict, List

from server.llm.client import invoke_llm
from server.llm.prompts.plan_refinement import PROMPT


def invoke_refinement_llm(plan: dict, issues: List[Dict[str, Any]]) -> dict:
    messages = [
        {"role": "system", "content": PROMPT},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "plan": plan,
                    "structuralIssues": issues,
                }
            ),
        },
    ]

    response = invoke_llm(
        messages=messages,
        temperature=0,
        response_format="json",
    )

    return response
