"""Pure helper functions: statistics and text formatting (no I/O)."""
from __future__ import annotations

from collections.abc import Sequence
from statistics import median

from app.models import Student


def _scores(students: Sequence[Student]) -> list[float]:
    """Single place that extracts scores (DRY)."""
    return [s.score for s in students]


def compute_stats(students: Sequence[Student]) -> dict[str, float | int | None]:
    """Return count, average, median, highest and lowest score (None when empty)."""
    scores = _scores(students)
    if not scores:
        return {"count": 0, "average": None, "median": None, "highest": None, "lowest": None}
    return {
        "count": len(scores),
        "average": round(sum(scores) / len(scores), 2),
        "median": median(scores),
        "highest": max(scores),
        "lowest": min(scores),
    }


def format_table(students: Sequence[Student]) -> str:
    """Render students as an aligned text table."""
    if not students:
        return "(no students)"
    width = max(len("Name"), *(len(s.name) for s in students))
    lines = [f"{'ID':>3} | {'Name':<{width}} | Score", f"{'-' * 3}-+-{'-' * width}-+-------"]
    lines += [f"{s.id:>3} | {s.name:<{width}} | {s.score:>5.1f}" for s in students]
    return "\n".join(lines)
