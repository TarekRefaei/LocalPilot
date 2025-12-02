"""
Standalone metrics server for LocalPilot.

Run this as a separate process to expose prometheus metrics on an isolated port.
Example:
  METRICS_BEARER_TOKEN=secret python backend/metrics_server.py --host 0.0.0.0 --port 9090
"""

from __future__ import annotations

import argparse
import logging
import os
import ssl
from http import HTTPStatus
from wsgiref.simple_server import WSGIRequestHandler, make_server

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

logger = logging.getLogger("metrics_server")

METRICS_TOKEN = os.environ.get("METRICS_BEARER_TOKEN")


def app(environ, start_response):
    # simple bearer token auth
    if METRICS_TOKEN:
        auth_header = environ.get("HTTP_AUTHORIZATION") or ""
        if not auth_header.startswith("Bearer "):
            start_response(
                f"{HTTPStatus.UNAUTHORIZED.value} Unauthorized",
                [("Content-Type", "text/plain")],
            )
            return [b"Unauthorized"]
        token = auth_header.split(" ", 1)[1]
        if token != METRICS_TOKEN:
            start_response(
                f"{HTTPStatus.FORBIDDEN.value} Forbidden",
                [("Content-Type", "text/plain")],
            )
            return [b"Forbidden"]

    data = generate_latest()
    start_response(f"{HTTPStatus.OK.value} OK", [("Content-Type", CONTENT_TYPE_LATEST)])
    return [data]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9090)
    parser.add_argument("--certfile", default=None)
    parser.add_argument("--keyfile", default=None)
    args = parser.parse_args()

    class QuietHandler(WSGIRequestHandler):
        def log_request(self, code="-", size="-"):
            # quiet logging
            pass

    logger.info("Starting metrics server on %s:%d", args.host, args.port)
    httpd = make_server(args.host, args.port, app, handler_class=QuietHandler)
    # Optional TLS
    if args.certfile and args.keyfile:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=args.certfile, keyfile=args.keyfile)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Metrics server shutting down")


if __name__ == "__main__":
    main()
