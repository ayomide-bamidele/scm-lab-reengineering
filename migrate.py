"""Migrate students from a JSON file into SQLite (idempotent).

Usage: python migrate.py [path/to/students.json]
"""
from __future__ import annotations

import json
import sys

from app.database import connect, db_path
from app.models import StudentIn


def migrate(json_file: str = "data/students.json") -> int:
    """Insert records that are not already in the database; return the number inserted."""
    with open(json_file, encoding="utf-8") as fh:
        records = [StudentIn(**r) for r in json.load(fh)]  # validates every record
    inserted = 0
    with connect() as conn:
        existing = {r["name"] for r in conn.execute("SELECT name FROM students")}
        for rec in records:
            if rec.name not in existing:
                conn.execute("INSERT INTO students (name, score) VALUES (?, ?)", (rec.name, rec.score))
                inserted += 1
    return inserted


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/students.json"
    print(f"Migrated {migrate(src)} record(s) from {src} into {db_path()}")
