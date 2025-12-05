def test_vector_store_defaults_to_settings_path(monkeypatch):
    # Lazy import inside test to ensure monkeypatching works on module attrs
    from app.core.config import settings

    captured = {}

    class DummyCollection:
        def count(self):
            return 0

    class DummyClient:
        def __init__(self, path=None, settings=None):
            captured["path"] = path
            self._settings = settings

        def get_or_create_collection(self, name, metadata):
            return DummyCollection()

    # Patch PersistentClient used inside the VectorStore module
    monkeypatch.setattr(
        "app.services.rag.vector_store.chromadb.PersistentClient", DummyClient
    )
    # Patch Path.mkdir used inside the VectorStore module to avoid disk writes
    monkeypatch.setattr(
        "app.services.rag.vector_store.Path.mkdir",
        lambda self, parents=False, exist_ok=False: None,
    )

    from app.services.rag.vector_store import VectorStore

    store = VectorStore()

    assert store.persist_directory == settings.vector_db_path
    assert captured["path"] == settings.vector_db_path
