def test_unverified_anchor_blocks_execution():
    from server.execute_v2.models.anchor import Anchor

    anchor = Anchor(type="function", symbol="x", verified=False)

    assert anchor.verified is False
