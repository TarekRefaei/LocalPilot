from __future__ import annotations

import time
from pathlib import Path

import aiosqlite

DB_PATH = Path(__file__).resolve().parents[2] / "localpilot_data.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
        CREATE TABLE IF NOT EXISTS chat_history (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          session_id TEXT,
          role TEXT,
          text TEXT,
          ts INTEGER
        )
        """
        )
        await db.commit()


async def save_message(
    session_id: str, role: str, text: str, ts: int | None = None
) -> None:
    if ts is None:
        ts = int(time.time())
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO chat_history (session_id, role, text, ts) VALUES (?, ?, ?, ?)",
            (session_id, role, text, ts),
        )
        await db.commit()


async def load_history(session_id: str, limit: int = 200):
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT role, text, ts FROM chat_history WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (session_id, limit),
        )
        rows = await cur.fetchall()
        return [{"role": r[0], "text": r[1], "ts": r[2]} for r in rows]
