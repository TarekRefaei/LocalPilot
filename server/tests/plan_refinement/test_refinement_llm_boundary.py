from server.plan.refinement.contracts import PlanRefinementProposal
from server.plan.refinement.validator import validate_and_apply_refinement


def test_llm_output_is_validated_before_apply():
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
                "reason": "break cycle",
            }
        ]
    }

    repaired = validate_and_apply_refinement(plan, PlanRefinementProposal(**proposal))

    a = next(t for t in repaired["tasks"] if t.get("id") == "a")
    assert a.get("dependencies") == []
