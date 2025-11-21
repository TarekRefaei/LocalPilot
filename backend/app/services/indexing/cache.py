from __future__ import annotations

import hashlib
import os
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileHashRecord:
    file_path: str
    hash: str
    size: int
    mtime: float
    language: str | None = None
    last_indexed: str | None = None
    doc_extracted: int = 0  # 0/1
    error: str | None = None


class FileHashCache:
    """SQLite-backed file-hash cache for incremental indexing."""

    def __init__(self, workspace_path: str) -> None:
        self.workspace = Path(workspace_path).resolve()
        self.cache_dir = self.workspace / ".localpilot"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "index_cache.sqlite"
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                """
        CREATE TABLE IF NOT EXISTS files (
          file_path TEXT PRIMARY KEY,
          hash TEXT NOT NULL,
          size INTEGER NOT NULL,
          mtime REAL NOT NULL,
          language TEXT,
          last_indexed TEXT,
          doc_extracted INTEGER DEFAULT 0,
          error TEXT
        );
        """
            )
            cur.execute(
                """
        CREATE TABLE IF NOT EXISTS runs (
          id TEXT PRIMARY KEY,
          started TEXT,
          ended TEXT,
          status TEXT,
          stats_json TEXT
        );
        """
            )
            cur.execute(
                """
        CREATE TABLE IF NOT EXISTS run_files (
          run_id TEXT,
          file_path TEXT,
          status TEXT,
          PRIMARY KEY (run_id, file_path)
        );
        """
            )
            con.commit()

    @staticmethod
    def normalize_path(workspace: Path, file_path: Path) -> str:
        rel = file_path.resolve().relative_to(workspace)
        # normalize to forward slashes and lower-case for Windows consistency
        return str(rel).replace(os.sep, "/")

    @staticmethod
    def hash_file(path: Path) -> tuple[str, int, float]:
        """Return (sha256_hex, size, mtime)."""
        h = hashlib.sha256()
        size = 0
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                size += len(chunk)
                h.update(chunk)
        mtime = path.stat().st_mtime
        return (h.hexdigest(), size, mtime)

    def get_all(self) -> dict[str, FileHashRecord]:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT file_path, hash, size, mtime, language, last_indexed, "
                "doc_extracted, error FROM files"
            )
            rows = cur.fetchall()
        out: dict[str, FileHashRecord] = {}
        for r in rows:
            out[r[0]] = FileHashRecord(
                file_path=r[0],
                hash=r[1],
                size=int(r[2]),
                mtime=float(r[3]),
                language=r[4],
                last_indexed=r[5],
                doc_extracted=int(r[6]) if r[6] is not None else 0,
                error=r[7],
            )
        return out

    def detect_changes(self, candidates: Iterable[Path]) -> tuple[list[str], list[str], list[str]]:
        """Return (added, modified, deleted) relative paths for candidate files."""
        existing = self.get_all()
        current: dict[str, tuple[str, int, float]] = {}

        added: list[str] = []
        modified: list[str] = []

        for p in candidates:
            rel = self.normalize_path(self.workspace, p)
            h, size, mtime = self.hash_file(p)
            current[rel] = (h, size, mtime)
            if rel not in existing:
                added.append(rel)
            else:
                prev = existing[rel]
                if prev.hash != h or prev.size != size or abs(prev.mtime - mtime) > 1e-6:
                    modified.append(rel)

        # deleted
        deleted = [rel for rel in existing.keys() if rel not in current]
        return added, modified, deleted

    def update_files(self, records: Iterable[FileHashRecord]) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.executemany(
                """
        INSERT INTO files (
          file_path, hash, size, mtime, language,
          last_indexed, doc_extracted, error
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
          hash=excluded.hash,
          size=excluded.size,
          mtime=excluded.mtime,
          language=excluded.language,
          last_indexed=excluded.last_indexed,
          doc_extracted=excluded.doc_extracted,
          error=excluded.error
        """,
                [
                    (
                        r.file_path,
                        r.hash,
                        int(r.size),
                        float(r.mtime),
                        r.language,
                        r.last_indexed,
                        int(r.doc_extracted),
                        r.error,
                    )
                    for r in records
                ],
            )
            con.commit()

    def record_run_start(self, run_id: str, started_iso: str) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO runs (id, started, status) VALUES (?, ?, ?)",
                (run_id, started_iso, "running"),
            )
            con.commit()

    def record_run_end(self, run_id: str, ended_iso: str, status: str, stats_json: str) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE runs SET ended = ?, status = ?, stats_json = ? WHERE id = ?",
                (ended_iso, status, stats_json, run_id),
            )
            con.commit()

    def record_run_file(self, run_id: str, file_path: str, status: str) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO run_files (run_id, file_path, status) VALUES (?, ?, ?)",
                (run_id, file_path, status),
            )
            con.commit()
