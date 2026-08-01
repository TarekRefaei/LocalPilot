from __future__ import annotations

import json
from typing import Any, Dict, List

from fastapi import HTTPException

from server.chat.ollama_chat_client import OllamaChatClient
from server.config.runtime import OLLAMA_BASE_URL
from server.plan.plan_parser import PlanParser
from server.plan.plan_validator import validate_plan_schema
from server.plan.plan_repair_prompt import build_plan_repair_prompt


def _assert_no_task_shape_change(original: Dict[str, Any], repaired: Dict[str, Any]) -> None:
    orig_tasks = original.get("tasks") or []
    rep_tasks = repaired.get("tasks") or []

    if not isinstance(orig_tasks, list) or not isinstance(rep_tasks, list):
        raise HTTPException(status_code=400, detail="Invalid plan shape")

    if len(orig_tasks) != len(rep_tasks):
        raise HTTPException(status_code=400, detail="Repair must not add or remove tasks")

    for i in range(len(orig_tasks)):
        o = orig_tasks[i] or {}
        r = rep_tasks[i] or {}
        if (o.get("id") != r.get("id")) or (o.get("orderIndex") != r.get("orderIndex")):
            raise HTTPException(status_code=400, detail="Repair must not change task order")


def repair_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    plan = payload.get("plan")
    warnings = payload.get("blockingWarnings")
    workspace = payload.get("workspace") or {}

    if not isinstance(plan, dict) or not isinstance(warnings, list) or not warnings:
        raise HTTPException(status_code=400, detail="Invalid repair payload")

    prompt = build_plan_repair_prompt(plan, warnings, workspace)

    client = OllamaChatClient(base_url=OLLAMA_BASE_URL, model="qwen2.5-coder:7b-instruct-q4_K_M")
    response = client.chat([
        {"role": "system", "content": prompt},
    ])

    parser = PlanParser()
    parsed = parser.parse(response)
    repaired = parsed.get("plan")

    if not repaired or not isinstance(repaired, dict):
        raise HTTPException(status_code=400, detail="LLM failed to produce valid plan")

    errors = validate_plan_schema(repaired)
    if errors:
        raise HTTPException(
            status_code=400,
            detail=f"Repaired plan invalid: {errors}",
        )

    _assert_no_task_shape_change(plan, repaired)

    return repaired
