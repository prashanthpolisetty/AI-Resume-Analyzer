from __future__ import annotations

import os
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("RESUME_ANALYZER_DB", Path(__file__).with_name("resume_analyzer.db")))


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect()) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                mode TEXT NOT NULL CHECK(mode IN ('targeted', 'general')),
                filename TEXT NOT NULL,
                job_title TEXT,
                score INTEGER NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_analyses_email_created
              ON analyses(email, created_at DESC);
            """
        )
        db.commit()


def save_analysis(*, email: str, mode: str, filename: str, job_title: str | None,
                  score: int, report_json: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(_connect()) as db:
        cursor = db.execute(
            """INSERT INTO analyses
               (email, mode, filename, job_title, score, report_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (email.lower().strip(), mode, filename, job_title, score, report_json, created_at),
        )
        db.commit()
        return int(cursor.lastrowid)


def list_analyses(email: str, limit: int = 20) -> list[dict[str, Any]]:
    with closing(_connect()) as db:
        rows = db.execute(
            """SELECT id, mode, filename, job_title, score, created_at
               FROM analyses WHERE email = ? ORDER BY created_at DESC LIMIT ?""",
            (email.lower().strip(), min(max(limit, 1), 100)),
        ).fetchall()
        return [dict(row) for row in rows]


def get_analysis(analysis_id: int, email: str) -> dict[str, Any] | None:
    with closing(_connect()) as db:
        row = db.execute(
            "SELECT * FROM analyses WHERE id = ? AND email = ?",
            (analysis_id, email.lower().strip()),
        ).fetchone()
        if not row:
            return None
        result = dict(row)
        import json
        result["report"] = json.loads(result.pop("report_json"))
        return result


def score_history(email: str) -> list[dict[str, Any]]:
    return [
        {"date": item["created_at"], "score": item["score"], "mode": item["mode"]}
        for item in reversed(list_analyses(email, 100))
    ]
