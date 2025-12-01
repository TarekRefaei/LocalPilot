## Prometheus scrape configuration for LocalPilot

If LocalPilot backend is reachable at `http://host:8765`, add this scrape config to your Prometheus `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: localpilot
    static_configs:
      - targets: ['localhost:8765']
    metrics_path: /metrics
    # optional: add bearer token via a file if you set METRICS_BEARER_TOKEN
    # bearer_token: /path/to/token/file
```

If you enabled `METRICS_BEARER_TOKEN` in LocalPilot, store the same token in a file and reference it via `bearer_token:` above.

### Separate metrics server
If you run the separate metrics server (recommended for separation), start it like:

```bash
METRICS_BEARER_TOKEN=your_token python backend/metrics_server.py --host 0.0.0.0 --port 9090
```

Then update Prometheus config:

```yaml
  - job_name: localpilot-metrics
    static_configs:
      - targets: ['metrics_host:9090']
    metrics_path: /metrics
    bearer_token: /path/to/token/file
```
