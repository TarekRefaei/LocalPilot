from server.plan.structure.graph_builder import build_plan_graph


def test_graph_builder_creates_nodes_and_edges():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": [],
            },
            {
                "id": "t2",
                "orderIndex": 1,
                "filePath": "b.py",
                "actionType": "modify",
                "dependencies": ["t1"],
            },
        ],
    }

    graph = build_plan_graph(plan)

    assert set(graph.nodes.keys()) == {"t1", "t2"}
    assert len(graph.edges) == 1
    assert graph.edges[0].source == "t1"
    assert graph.edges[0].target == "t2"
