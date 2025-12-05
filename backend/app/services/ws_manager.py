"""
WebSocket connection manager for handling client connections and message routing.
"""

import json
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and message routing."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.subscriptions: dict[str, set[str]] = {}  # event -> set of client_ids

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client connected: {client_id}")

    def disconnect(self, client_id: str) -> None:
        """Remove a disconnected client."""
        self.active_connections.pop(client_id, None)
        # Clean up subscriptions
        for subscribers in self.subscriptions.values():
            subscribers.discard(client_id)
        logger.info(f"Client disconnected: {client_id}")

    async def send_personal(self, client_id: str, message: dict) -> None:
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")

    async def broadcast(self, message: dict) -> None:
        """Broadcast a message to all connected clients."""
        disconnected_clients = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

    async def broadcast_to_topic(self, event: str, message: dict) -> None:
        """Broadcast a message to all clients subscribed to an event topic."""
        subscribers = self.subscriptions.get(event, set())
        disconnected_clients = []

        for client_id in subscribers:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_text(
                        json.dumps(message)
                    )
                except Exception as e:
                    logger.error(f"Error sending to {client_id}: {e}")
                    disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

    def subscribe(self, client_id: str, event: str) -> None:
        """Subscribe a client to an event topic."""
        if event not in self.subscriptions:
            self.subscriptions[event] = set()
        self.subscriptions[event].add(client_id)
        logger.debug(f"Client {client_id} subscribed to {event}")

    def unsubscribe(self, client_id: str, event: str) -> None:
        """Unsubscribe a client from an event topic."""
        if event in self.subscriptions:
            self.subscriptions[event].discard(client_id)
            logger.debug(f"Client {client_id} unsubscribed from {event}")

    def get_connected_clients(self) -> list[str]:
        """Get list of connected client IDs."""
        return list(self.active_connections.keys())

    def get_client_count(self) -> int:
        """Get number of connected clients."""
        return len(self.active_connections)
