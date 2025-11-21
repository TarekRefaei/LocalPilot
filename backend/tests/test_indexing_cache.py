from __future__ import annotations

import time
from pathlib import Path

from app.services.indexing.cache import FileHashCache, FileHashRecord


def test_filehashcache_added_modified_deleted(tmp_path: Path) -> None:
    ws = tmp_path
    f1 = ws / "a.txt"
    f2 = ws / "b.txt"
    f1.write_text("hello", encoding="utf-8")
    f2.write_text("world", encoding="utf-8")

    cache = FileHashCache(str(ws))

    # First scan: both are added
    added, modified, deleted = cache.detect_changes([f1, f2])
    assert sorted(added) == sorted(
        [
            FileHashCache.normalize_path(ws, f1),
            FileHashCache.normalize_path(ws, f2),
        ]
    )
    assert modified == []
    assert deleted == []

    # Update cache
    recs = []
    for p in [f1, f2]:
        h, size, mtime = cache.hash_file(p)
        recs.append(
            FileHashRecord(
                file_path=FileHashCache.normalize_path(ws, p),
                hash=h,
                size=size,
                mtime=mtime,
            )
        )
    cache.update_files(recs)

    # Modify one file
    time.sleep(0.01)
    f1.write_text("hello2", encoding="utf-8")

    # Delete another file
    f2.unlink()

    # Detect changes
    added, modified, deleted = cache.detect_changes([f1])
    assert added == []
    assert FileHashCache.normalize_path(ws, f1) in modified
    assert FileHashCache.normalize_path(ws, f2) in deleted
