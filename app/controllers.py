"""Application layer: use cases that combine models, utils and the database."""
from __future__ import annotations

from app.database import connect
from app.models import Student, StudentIn
from app.utils import compute_stats


def add_student(payload: StudentIn) -> Student:
    """Insert a validated student and return it with its id."""
    with connect() as conn:
        cur = conn.execute("INSERT INTO students (name, score) VALUES (?, ?)", (payload.name, payload.score))
        return Student(id=cur.lastrowid, name=payload.name, score=payload.score)


def list_students() -> list[Student]:
    """Return all students ordered by id."""
    with connect() as conn:
        rows = conn.execute("SELECT id, name, score FROM students ORDER BY id").fetchall()
    return [Student(**dict(r)) for r in rows]


def get_student(student_id: int) -> Student | None:
    """Return one student or None."""
    with connect() as conn:
        row = conn.execute("SELECT id, name, score FROM students WHERE id = ?", (student_id,)).fetchone()
    return Student(**dict(row)) if row else None


def delete_student(student_id: int) -> bool:
    """Delete a student; True if a row was removed."""
    with connect() as conn:
        return conn.execute("DELETE FROM students WHERE id = ?", (student_id,)).rowcount > 0


def stats() -> dict[str, float | int | None]:
    """Statistics over every stored student."""
    return compute_stats(list_students())
