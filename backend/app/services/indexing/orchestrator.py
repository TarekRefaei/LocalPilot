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
from .discovery import DiscoveryExecutor
from .documentation import DocumentationExtractor


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
                "added": len(added),
                "modified": len(modified),
                "deleted": len(deleted),
                "estimated_seconds": dres.estimated_duration_seconds,
            }

            await self._emit_complete(indexing_id, duration, stats)

        except Exception as e:
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
