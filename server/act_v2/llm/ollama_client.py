import requests
from typing import List, Dict


class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def invoke(self, messages: List[Dict]) -> str:
        r = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "top_p": 1,
                    "num_ctx": 8192,
                    "repeat_penalty": 1.0,
                }
            },
            timeout=180
        )
        r.raise_for_status()
        return (r.json().get("message") or {}).get("content", "")
