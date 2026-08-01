import pytest

from server.plan.refinement.contracts import PlanRefinementProposal
from server.plan.refinement.validator import validate_and_apply_refinement, RefinementValidationError
from server.plan.structure.diagnostics import analyze_plan_structure


def test_refinement_breaks_cycle():
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "a", "orderIndex": 0, "dependencies": ["b"]},
            {"id": "b", "orderIndex": 1, "dependencies": ["a"]},
        ],
    }

    proposal = {
        "repairs": [
            {
                "kind": "remove_dependency",
                "taskId": "a",
                "dependency": "b",
                "reason": "Break cycle",
            }
        ]
    }

    repaired = validate_and_apply_refinement(plan, PlanRefinementProposal(**proposal))

    issues = analyze_plan_structure(repaired)
    assert not issues


def test_refinement_rejects_noop_remove_dependency():
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "a", "orderIndex": 0, "dependencies": []},
            {"id": "b", "orderIndex": 1, "dependencies": []},
        ],
    }

    proposal = {
        "repairs": [
            {
                "kind": "remove_dependency",
                "taskId": "a",
                "dependency": "b",
                "reason": "Break cycle",
            }
        ]
    }

    with pytest.raises(RefinementValidationError):
        validate_and_apply_refinement(plan, PlanRefinementProposal(**proposal))


def test_refinement_rejects_duplicate_repairs():
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "a", "orderIndex": 0, "dependencies": ["b"]},
            {"id": "b", "orderIndex": 1, "dependencies": []},
        ],
    }

    proposal = {
        "repairs": [
            {
                "kind": "remove_dependency",
                "taskId": "a",
                "dependency": "b",
                "reason": "Break cycle",
            },
            {
                "kind": "remove_dependency",
                "taskId": "a",
                "dependency": "b",
                "reason": "Break cycle",
            },
        ]
    }

    with pytest.raises(RefinementValidationError):
        validate_and_apply_refinement(plan, PlanRefinementProposal(**proposal))


def test_refinement_rejects_structural_regression():
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "a", "orderIndex": 0, "dependencies": []},
            {"id": "b", "orderIndex": 1, "dependencies": []},
        ],
    }

    proposal = {
        "repairs": [
            {
                "kind": "add_dependency",
                "taskId": "a",
                "dependency": "ghost",
                "reason": "Test",
            }
        ]
    }

    with pytest.raises(RefinementValidationError):
        validate_and_apply_refinement(plan, PlanRefinementProposal(**proposal))
