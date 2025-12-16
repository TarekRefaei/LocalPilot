import json
import requests
from typing import Iterable, Dict


class OllamaChatClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def stream_chat(self, messages: Iterable[Dict]) -> Iterable[str]:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": list(messages),
                "stream": True
            },
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                yield data["message"]["content"]
