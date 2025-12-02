# Metrics and model discovery

## Environment variables
- `OLLAMA_URL` (default `http://127.0.0.1:11434`) — URL of Ollama server
- `OLLAMA_API_KEY` — optional API key (added as `Authorization: Bearer <key>`)
- `OLLAMA_VERIFY_SSL` — set `0` or `false` to disable TLS verification (not recommended)
- `METRICS_BEARER_TOKEN` — optional bearer token to protect `/metrics` endpoint

## Model discovery
- The extension queries `/api/models` on the backend to fetch available models from Ollama.
- Use the command `LocalPilot: Swap Model` in the Command Palette to pick a model. This selection is persisted via the extension's MementoState.

## Prometheus
- See `docs/prometheus_scrape.md` for an example scrape configuration.
