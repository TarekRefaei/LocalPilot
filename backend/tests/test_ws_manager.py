import json

import pytest

from app.services.ws_manager import ConnectionManager


class FakeWebSocket:
    def __init__(self, should_fail: bool = False, store: list[str] | None = None):
        self.should_fail = should_fail
        self.accepted = False
        self.store = store if store is not None else []

    async def accept(self):
        self.accepted = True

    async def send_text(self, text: str):
        if self.should_fail:
            raise RuntimeError("boom")
        # store sent messages for assertions
        self.store.append(text)


@pytest.mark.asyncio
async def test_connect_disconnect_and_counts():
    mgr = ConnectionManager()
    ws = FakeWebSocket()

    await mgr.connect("c1", ws)
    assert ws.accepted is True
    assert mgr.get_connected_clients() == ["c1"]
    assert mgr.get_client_count() == 1

    # subscribe and ensure cleaned on disconnect
    mgr.subscribe("c1", "topic.a")
    assert "c1" in mgr.subscriptions.get("topic.a", set())

    mgr.disconnect("c1")
    assert mgr.get_client_count() == 0
    assert "c1" not in mgr.subscriptions.get("topic.a", set())


@pytest.mark.asyncio
async def test_send_personal_success_and_error_logging():
    mgr = ConnectionManager()
    sent: list[str] = []
    ok_ws = FakeWebSocket(store=sent)
    bad_ws = FakeWebSocket(should_fail=True)

    await mgr.connect("ok", ok_ws)
    await mgr.connect("bad", bad_ws)

    await mgr.send_personal("ok", {"event": "hello"})
    # message serialized to json and stored
    assert any(json.loads(x)["event"] == "hello" for x in sent)

    # error path shouldn't raise
    await mgr.send_personal("bad", {"event": "fail"})
    # still connected (send_personal does not disconnect)
    assert "bad" in mgr.get_connected_clients()


@pytest.mark.asyncio
async def test_broadcast_cleans_disconnected_clients():
    mgr = ConnectionManager()
    sent: list[str] = []
    ok_ws = FakeWebSocket(store=sent)
    bad_ws = FakeWebSocket(should_fail=True)

    await mgr.connect("ok", ok_ws)
    await mgr.connect("bad", bad_ws)

    await mgr.broadcast({"event": "broadcast.me"})

    # ok client received it
    assert any(json.loads(x)["event"] == "broadcast.me" for x in sent)
    # bad client should be disconnected after failure
    assert "bad" not in mgr.get_connected_clients()


@pytest.mark.asyncio
async def test_broadcast_to_topic_filters_and_cleans():
    mgr = ConnectionManager()
    sent_a: list[str] = []
    ws_a = FakeWebSocket(store=sent_a)
    ws_b = FakeWebSocket(should_fail=True)

    await mgr.connect("A", ws_a)
    await mgr.connect("B", ws_b)

    mgr.subscribe("A", "topic.x")
    mgr.subscribe("B", "topic.x")

    await mgr.broadcast_to_topic("topic.x", {"event": "topic.x", "data": 1})

    # A got it, B failed and was removed
    assert any(json.loads(x)["event"] == "topic.x" for x in sent_a)
    assert "B" not in mgr.get_connected_clients()

    # unsubscribe path
    mgr.unsubscribe("A", "topic.x")
    assert "A" not in mgr.subscriptions.get("topic.x", set())
