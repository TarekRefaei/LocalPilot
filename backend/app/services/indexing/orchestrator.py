from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models.envelope import (
    IndexingCompletePayload,
    IndexingProgressPayload,
    WebSocketEnvelope,
)
from app.services.ws_manager import ConnectionManager

from .cache import FileHashCache, FileHashRecord
from .chunking import ChunkingExecutor
from .discovery import DiscoveryExecutor
from .documentation import DocumentationExtractor
from .symbol_map import SymbolImportMapBuilder


class IndexingOrchestrator:
    def __init__(self, manager: ConnectionManager) -> None:
        self.manager = manager

    async def run(self, workspace_path: str, options: dict[str, Any] | None = None) -> None:
        indexing_id = str(uuid.uuid4())
        started = datetime.utcnow()

        try:
            discovery = DiscoveryExecutor()
            doc = DocumentationExtractor()
            cache = FileHashCache(workspace_path)
            chunking = ChunkingExecutor()

            await self._emit_progress(
                indexing_id,
                phase="DISCOVERY",
                phase_number=1,
                total_phases=5,
                current_file=0,
                total_files=0,
                current_file_path=None,
                percentage=2.0,
                message="Starting discovery",
            )

            dres = await discovery.execute(workspace_path)

            await self._emit_progress(
                indexing_id,
                phase="DISCOVERY",
                phase_number=1,
                total_phases=5,
                current_file=0,
                total_files=dres.total_files,
                current_file_path=None,
                percentage=10.0,
                message=f"Discovered {dres.total_files} files in {dres.project_type} project",
            )

            added, modified, deleted = cache.detect_changes(dres.files)

            total_to_process = len(added) + len(modified)
            processed = 0

            md_files = doc.find_markdown_files(dres.files)
            code_files = doc.find_code_files(dres.files)
            total_docs = 0

            for f in md_files:
                chunks = doc.process_markdown(f, workspace_path)
                total_docs += len(chunks)
                processed += 1
                await self._emit_progress(
                    indexing_id,
                    phase="DOCUMENTATION",
                    phase_number=2,
                    total_phases=5,
                    current_file=processed,
                    total_files=max(1, total_to_process),
                    current_file_path=str(Path(f).resolve()),
                    percentage=min(90.0, 10.0 + 80.0 * (processed / max(1, total_to_process))),
                    message=f"Processed documentation: {f.name}",
                )

            for f in code_files:
                chunks = doc.extract_docstrings(f, workspace_path)
                total_docs += len(chunks)
                processed += 1
                await self._emit_progress(
                    indexing_id,
                    phase="DOCUMENTATION",
                    phase_number=2,
                    total_phases=5,
                    current_file=processed,
                    total_files=max(1, total_to_process),
                    current_file_path=str(Path(f).resolve()),
                    percentage=min(95.0, 10.0 + 80.0 * (processed / max(1, total_to_process))),
                    message=f"Extracted docstrings: {f.name}",
                )

            # Phase 4: Semantic Chunking
            await self._emit_progress(
                indexing_id,
                phase="CHUNKING",
                phase_number=4,
                total_phases=5,
                current_file=0,
                total_files=len(dres.files),
                current_file_path=None,
                percentage=50.0,
                message="Starting semantic code chunking...",
            )

            code_chunks, chunk_metrics = await chunking.execute(workspace_path, dres.files)

            await self._emit_progress(
                indexing_id,
                phase="CHUNKING",
                phase_number=4,
                total_phases=5,
                current_file=len(dres.files),
                total_files=len(dres.files),
                current_file_path=None,
                percentage=80.0,
                message=f"Created {len(code_chunks)} semantic chunks with symbol/import maps",
            )

            # Build symbol and import maps
            symbol_map, import_map = SymbolImportMapBuilder.build(code_chunks)

            # Phase 5: Embeddings & Vector Store
            await self._emit_progress(
                indexing_id,
                phase="EMBEDDINGS",
                phase_number=5,
                total_phases=5,
                current_file=0,
                total_files=len(code_chunks),
                current_file_path=None,
                percentage=80.0,
                message="Starting embeddings generation...",
            )

            # Initialize embedding services (lazy import to avoid circular dependency)
            from app.services.rag.embedding_executor import EmbeddingExecutor
            from app.services.rag.embedding_service import EmbeddingService
            from app.services.rag.vector_store import VectorStore

            embedding_service = EmbeddingService(
                ollama_base_url="http://localhost:11434",
                batch_size=32,
            )
            vector_store = VectorStore(
                persist_directory=str(Path(workspace_path) / ".localpilot" / "vectordb"),
                collection_name="localpilot_codebase",
            )
            embedding_executor = EmbeddingExecutor(
                embedding_service=embedding_service,
                vector_store=vector_store,
                batch_size=32,
            )

            # Define progress callback for embeddings
            def embedding_progress_callback(event: dict[str, Any]) -> None:
                if event.get("status") == "in_progress":
                    percentage = event.get("percentage", 80.0)
                    batch_num = event.get("batch_number", 0)
                    total_batches = event.get("total_batches", 1)
                    await_coro = self._emit_progress(
                        indexing_id,
                        phase="EMBEDDINGS",
                        phase_number=5,
                        total_phases=5,
                        current_file=event.get("chunks_processed", 0),
                        total_files=event.get("total_chunks", len(code_chunks)),
                        current_file_path=None,
                        percentage=80.0 + (percentage * 0.2),  # 80-100%
                        message=f"Embedding batch {batch_num}/{total_batches}",
                    )
                    # Schedule coroutine to run
                    import asyncio
                    asyncio.create_task(await_coro)

            # Execute embeddings
            embedding_result = await embedding_executor.execute(
                code_chunks,
                progress_callback=embedding_progress_callback,
            )

            embedded_count = embedding_result.get("embedded_chunks", 0)
            await self._emit_progress(
                indexing_id,
                phase="EMBEDDINGS",
                phase_number=5,
                total_phases=5,
                current_file=len(code_chunks),
                total_files=len(code_chunks),
                current_file_path=None,
                percentage=100.0,
                message=f"Generated embeddings for {embedded_count} chunks",
            )

            # Update cache with file hashes
            records: list[FileHashRecord] = []
            for p in dres.files:
                rel = cache.normalize_path(Path(workspace_path).resolve(), p)
                h, size, mtime = cache.hash_file(p)
                records.append(FileHashRecord(file_path=rel, hash=h, size=size, mtime=mtime))
            cache.update_files(records)

            duration = int((datetime.utcnow() - started).total_seconds())
            stats = {
                "total_files": dres.total_files,
                "files_by_type": dres.files_by_type,
                "project_type": dres.project_type,
                "docs_chunks": total_docs,
                "code_chunks": len(code_chunks),
                "chunk_types": chunk_metrics.get("chunk_types", {}),
                "avg_chunk_tokens": chunk_metrics.get("avg_tokens", 0),
                "total_symbols": symbol_map.to_dict()["total_symbols"],
                "total_imports": import_map.to_dict()["total_imports"],
                "embedded_chunks": embedding_result.get("embedded_chunks", 0),
                "embedding_failed_chunks": embedding_result.get("failed_chunks", 0),
                "added": len(added),
                "modified": len(modified),
                "deleted": len(deleted),
                "estimated_seconds": dres.estimated_duration_seconds,
            }

            await self._emit_complete(indexing_id, duration, stats)

        except Exception as e:
            import traceback

            traceback.print_exc()
            duration = int((datetime.utcnow() - started).total_seconds())
            stats = {"error": str(e)}
            await self._emit_complete(indexing_id, duration, stats)

    async def _emit_progress(
        self,
        indexing_id: str,
        phase: str,
        phase_number: int,
        total_phases: int,
        current_file: int,
        total_files: int,
        current_file_path: str | None,
        percentage: float,
        message: str,
    ) -> None:
        payload = IndexingProgressPayload(
            indexing_id=indexing_id,
            phase=phase,
            phase_number=phase_number,
            total_phases=total_phases,
            current_file=current_file,
            total_files=total_files,
            current_file_path=current_file_path,
            percentage=float(f"{percentage:.2f}"),
            estimated_time_remaining_seconds=max(0, 0),
            message=message,
        )
        envelope = WebSocketEnvelope(event="indexing.progress", data=payload.model_dump())
        await self.manager.broadcast(envelope.model_dump())

    async def _emit_complete(
        self,
        indexing_id: str,
        duration_seconds: int,
        statistics: dict[str, Any],
    ) -> None:
        payload = IndexingCompletePayload(
            indexing_id=indexing_id,
            duration_seconds=duration_seconds,
            statistics=statistics,
            project_summary=None,
            failed_files=None,
        )
        envelope = WebSocketEnvelope(event="indexing.complete", data=payload.model_dump())
        await self.manager.broadcast(envelope.model_dump())
