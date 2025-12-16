from pathlib import Path

from .scanner import WorkspaceScanner
from .language import detect_language
from .chunker import SemanticChunker
from .hash_tracker import hash_file
from .state import IndexState
from .vector_store import VectorStore


class IndexingService:
    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        embedder,
        progress=None
    ):
        self.workspace = workspace
        self.index_root = index_root
        self.embedder = embedder
        self.progress = progress

        self.scanner = WorkspaceScanner()
        self.chunker = SemanticChunker()

    def run(self) -> None:
        state = IndexState(self.index_root)
        state.load()

        files = self.scanner.scan(self.workspace)
        total_files = len(files)

        all_chunks = []
        texts = []

        for idx, path in enumerate(files, start=1):
            if self.progress:
                self.progress.report("scan", idx, total_files)

            current_hash = hash_file(path)
            stored_hash = state.file_hashes.get(str(path))

            if stored_hash == current_hash:
                continue

            language = detect_language(path)
            if not language:
                continue

            source = path.read_text(encoding="utf-8", errors="ignore")

            chunks = self.chunker.chunk_file(
                file_path=str(path),
                language=language,
                source=source
            )

            all_chunks.extend(chunks)
            texts.extend([c.content for c in chunks])

            state.file_hashes[str(path)] = current_hash
            if self.progress:
                self.progress.report("chunk", idx, total_files)

        if not all_chunks:
            if self.progress:
                self.progress.report("complete", total_files, total_files)
            return

        if self.progress:
            self.progress.report("embed", 0, len(texts))

        embeddings = self.embedder.embed(texts)

        if self.progress:
            self.progress.report("store", 0, len(all_chunks))

        store = VectorStore(
            persist_dir=str(self.index_root / "chroma"),
            collection_name="code_chunks"
        )
        store.add(all_chunks, embeddings)

        state.save()

        if self.progress:
            self.progress.report("complete", total_files, total_files)
