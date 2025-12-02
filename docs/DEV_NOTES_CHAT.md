## Replacing the mock chat model with a real model adapter

Files to update:

- `backend/app/api/chat.py` : replace `_mock_model_generate` with a real generator that streams tokens from your model.
- `backend/app/services/rag/*` : ensure `MultiLevelRetriever.retrieve` returns chunks with `content` (strings). If not, adapt in `chat.py`.

Tips:
- Keep `StreamingResponse` and yield tokens as they become available.
- If using Ollama or llama.cpp, create an async iterator that yields text pieces (or stream fixed-size chunks of a sync response).
