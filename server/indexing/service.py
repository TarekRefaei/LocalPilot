from pathlib import Path

from .scanner import WorkspaceScanner
from .language import detect_language
from .chunker import SemanticChunker
from .hash_tracker import hash_file
from .state import IndexState
from .vector_store import VectorStore
from .symbol_index import SymbolIndex
from .summary_service import SummaryService


class IndexingService:
    """
    Phase 2.5
    ----------
    Produces:
    - Vector index (semantic chunks)
    - Symbol index (structure)
    - Project summary (knowledge)
    """

    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        embedder,
        progress=None,
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
        symbol_index = SymbolIndex(self.index_root)

        # ==================================================
        # Scan & chunk
        # ==================================================
        for idx, path in enumerate(files, start=1):
            if self.progress:
                self.progress.report("scan", idx, total_files)

            current_hash = hash_file(path)
            if state.file_hashes.get(str(path)) == current_hash:
                continue

            language = detect_language(path)
            if not language:
                continue

            source = path.read_text(encoding="utf-8", errors="ignore")

            chunks = self.chunker.chunk_file(
                file_path=str(path),
                language=language,
                source=source,
            )

            for c in chunks:
                if not c.content or not c.content.strip():
                    continue
                if len(c.content.strip()) < 10:
                    continue

                all_chunks.append(c)
                texts.append(c.content)

                if c.symbol_type != "file":
                    symbol_index.add_chunk(c)

            state.file_hashes[str(path)] = current_hash

            if self.progress:
                self.progress.report("chunk", idx, total_files)

        # ==================================================
        # Nothing new → still persist structure
        # ==================================================
        if not all_chunks:
            symbol_index.save()
            state.save()
            if self.progress:
                self.progress.report("complete", total_files, total_files)
            return

        # ==================================================
        # Embed
        # ==================================================
        embeddings = self.embedder.embed(texts)

        if len(embeddings) != len(all_chunks):
            raise RuntimeError(
                f"Embedding mismatch: {len(embeddings)} embeddings "
                f"for {len(all_chunks)} chunks"
            )

        for i, emb in enumerate(embeddings):
            if not emb:
                c = all_chunks[i]
                raise RuntimeError(
                    f"Empty embedding for chunk "
                    f"{c.file_path}:{c.start_line}-{c.end_line}"
                )

        # ==================================================
        # Store vectors
        # ==================================================
        ids = [c.id for c in all_chunks]
        if len(ids) != len(set(ids)):
            raise RuntimeError("Duplicate chunk IDs detected before vector insert")

        store = VectorStore(
            persist_dir=str(self.index_root / "chroma"),
            collection_name="code_chunks",
        )
        store.add(all_chunks, embeddings)

        # ==================================================
        # Persist structure & knowledge
        # ==================================================
        symbol_index.save()

        SummaryService(
            workspace=self.workspace,
            index_root=self.index_root,
        ).generate_and_save()

        state.save()

        if self.progress:
            self.progress.report("complete", total_files, total_files)
    