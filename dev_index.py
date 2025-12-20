from pathlib import Path
from server.indexing.service import IndexingService
from server.api.dependencies import get_index_root, get_embedder

if __name__ == "__main__":
    workspace = Path(
        r"C:\Users\super\OneDrive\Desktop\My Projects\test_project"
    )

    print(f"Indexing workspace: {workspace}")

    IndexingService(
        workspace=workspace,
        index_root=get_index_root() / "default",
        embedder=get_embedder(),
    ).run()

    print("Indexing complete.")


# from pathlib import Path
# from server.indexing.service import IndexingService
# from server.api.dependencies import get_embedder, get_index_root

# workspace = Path(".").resolve()   # repo root
# project_id = "default"

# index_root = get_index_root() / project_id
# embedder = get_embedder()

# print("Indexing workspace:", workspace)
# IndexingService(
#     workspace=workspace,
#     index_root=index_root,
#     embedder=embedder,
# ).run()

# print("Indexing complete.")
# print("Index root:", index_root)
