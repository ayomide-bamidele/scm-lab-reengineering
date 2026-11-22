"""Console report (replaces the old app.py). Run: python -m app.cli"""
from __future__ import annotations

from app import controllers
from app.utils import format_table


def main() -> None:
    """Print the student table and summary statistics."""
    students = controllers.list_students()
    s = controllers.stats()
    print("=== Student Report (SQLite) ===")
    print(format_table(students))
    print("-" * 24)
    print(f"Count   : {s['count']}")
    print(f"Average : {s['average']}")
    print(f"Median  : {s['median']}")
    print(f"Highest : {s['highest']}")
    print(f"Lowest  : {s['lowest']}")


if __name__ == "__main__":
    main()
