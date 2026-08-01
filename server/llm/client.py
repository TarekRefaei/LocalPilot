import json
from typing import List, Dict, Any

import requests

from server.config.runtime import OLLAMA_BASE_URL


def invoke_llm(
    messages: List[Dict[str, Any]],
    temperature: float = 0,
    response_format: str = "json",
    model: str = "qwen2.5-coder:7b-instruct-q4_K_M",
) -> dict:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    if response_format == "json":
        payload["format"] = "json"

    r = requests.post(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat",
        json=payload,
        timeout=180,
    )
    r.raise_for_status()

    content = (r.json().get("message") or {}).get("content", "")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("LLM returned empty response")

    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(f"LLM returned non-JSON content: {content[:200]}") from e
