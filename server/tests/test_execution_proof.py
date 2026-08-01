def test_execution_without_proof_is_rejected():
    from server.execute_v2.models.execution_state import ExecutionState
    from server.execute_v2.proof.plan_execution_proof import verify_execution_proof

    state = ExecutionState(
        execution_id="x",
        plan_id="p",
        plan_title="t",
        status="running",
        tasks=[],
        context={},
        proof=None,
    )

    try:
        verify_execution_proof(state)
        assert False, "Execution without proof must fail"
    except Exception:
        pass
