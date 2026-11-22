"""SQLite access layer."""
from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 100)
)
"""


def db_path() -> str:
    """Database file location (override with the STUDENTS_DB environment variable)."""
    return os.environ.get("STUDENTS_DB", "data/students.db")


@contextmanager
def connect(path: str | None = None) -> Iterator[sqlite3.Connection]:
    """Yield a connection with the schema ensured; commit on success, always close."""
    target = path or db_path()
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()
