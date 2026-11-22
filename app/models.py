"""Domain models for the students service."""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class StudentIn(BaseModel):
    """Payload used to create a student (validated)."""

    name: str = Field(min_length=1, examples=["Ada"])
    score: float = Field(ge=0, le=100, examples=[91])

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        """Trim whitespace and reject blank names."""
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value


class Student(StudentIn):
    """A persisted student with its database id."""

    id: int
