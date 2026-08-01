import pytest
from fastapi import HTTPException

from server.plan.repair import repair_plan


VALID_PLAN = {
    "id": "p1",
    "title": "Test",
    "overview": "Test plan",
    "tasks": [
        {
            "id": "t1",
            "orderIndex": 0,
            "title": "Create file",
            "description": "",
            "filePath": "a.py",
            "actionType": "create",
            "details": [],
            "dependencies": [],
        }
    ],
    "status": "draft",
}


def _payload(plan, response_markdown):
    return {
        "plan": plan,
        "blockingWarnings": [{"code": "file_already_exists"}],
        "workspace": {"existingFiles": []},
        "_mock_llm_response": response_markdown,
    }


def _patch_llm(monkeypatch, *, response_text: str):
    from server.chat.ollama_chat_client import OllamaChatClient

    def _chat(self, messages):
        return response_text

    monkeypatch.setattr(OllamaChatClient, "chat", _chat)


def _as_markdown(plan_dict):
    import json

    return "```json\n" + json.dumps(plan_dict) + "\n```"


def test_repair_does_not_change_task_count(monkeypatch):
    bad = dict(VALID_PLAN)
    bad["tasks"] = []

    _patch_llm(monkeypatch, response_text=_as_markdown(bad))

    with pytest.raises(HTTPException) as e:
        repair_plan({
            "plan": VALID_PLAN,
            "blockingWarnings": [{"code": "file_already_exists"}],
            "workspace": {"existingFiles": []},
        })

    assert e.value.status_code == 400


def test_repair_rejects_task_reorder(monkeypatch):
    bad = {
        **VALID_PLAN,
        "tasks": [
            {
                **VALID_PLAN["tasks"][0],
                "orderIndex": 1,
            }
        ],
    }

    _patch_llm(monkeypatch, response_text=_as_markdown(bad))

    with pytest.raises(HTTPException) as e:
        repair_plan({
            "plan": VALID_PLAN,
            "blockingWarnings": [{"code": "file_already_exists"}],
            "workspace": {"existingFiles": []},
        })

    assert e.value.status_code == 400


def test_repair_rejects_invalid_schema(monkeypatch):
    bad = {"foo": "bar"}

    _patch_llm(monkeypatch, response_text=_as_markdown(bad))

    with pytest.raises(HTTPException) as e:
        repair_plan({
            "plan": VALID_PLAN,
            "blockingWarnings": [{"code": "file_already_exists"}],
            "workspace": {"existingFiles": []},
        })

    assert e.value.status_code == 400


def test_repair_rejects_invalid_json(monkeypatch):
    _patch_llm(monkeypatch, response_text="not json")

    with pytest.raises(HTTPException) as e:
        repair_plan({
            "plan": VALID_PLAN,
            "blockingWarnings": [{"code": "file_already_exists"}],
            "workspace": {"existingFiles": []},
        })

    assert e.value.status_code == 400


def test_repair_accepts_valid_plan(monkeypatch):
    good = {
        **VALID_PLAN,
        "tasks": [
            {
                **VALID_PLAN["tasks"][0],
                "actionType": "modify",
            }
        ],
    }

    _patch_llm(monkeypatch, response_text=_as_markdown(good))

    repaired = repair_plan({
        "plan": VALID_PLAN,
        "blockingWarnings": [{"code": "file_already_exists"}],
        "workspace": {"existingFiles": []},
    })

    assert isinstance(repaired, dict)
    assert len(repaired.get("tasks") or []) == 1
    assert repaired["tasks"][0]["id"] == "t1"
    assert repaired["tasks"][0]["orderIndex"] == 0
    assert repaired["tasks"][0]["actionType"] == "modify"
