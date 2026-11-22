"""FastAPI REST interface. Run: uvicorn app.main:app --reload"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response

from app import controllers
from app.models import Student, StudentIn

app = FastAPI(title="Students API", version="2.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe used by Docker."""
    return {"status": "ok"}


@app.get("/students", response_model=list[Student])
def list_students() -> list[Student]:
    """List all students."""
    return controllers.list_students()


@app.post("/students", response_model=Student, status_code=201)
def create_student(payload: StudentIn) -> Student:
    """Create a student (422 on invalid name or score)."""
    return controllers.add_student(payload)


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int) -> Student:
    """Fetch one student or 404."""
    student = controllers.get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id}", status_code=204)
def remove_student(student_id: int) -> Response:
    """Delete a student or 404."""
    if not controllers.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=204)


@app.get("/stats")
def read_stats() -> dict:
    """Average, median, highest, lowest and count."""
    return controllers.stats()
