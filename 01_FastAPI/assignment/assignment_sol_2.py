"""
FastAPI endpoint that accepts a list of course objects and stores them in a
JSON file, using a Pydantic model to validate each course.
"""

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Course Catalog API",
    description="Accepts course objects and persists them to a JSON file.",
    version="1.0.0",
)

COURSES_FILE = Path(__file__).parent / "courses.json"


# ── Pydantic model ───────────────────────────────────────────────────
class Course(BaseModel):
    course_id: int = Field(..., gt=0, description="Unique course identifier")
    course_name: str = Field(..., min_length=1, description="Name of the course")
    credits: int = Field(..., gt=0, le=10, description="Number of credits, 1-10")
    instructor: str = Field(..., min_length=1, description="Instructor's name")


# ── Storage helpers ──────────────────────────────────────────────────
def load_courses() -> List[dict]:
    if not COURSES_FILE.exists():
        return []
    with open(COURSES_FILE, "r") as f:
        return json.load(f)


def save_courses(courses: List[dict]) -> None:
    with open(COURSES_FILE, "w") as f:
        json.dump(courses, f, indent=2)


# ── API endpoint ─────────────────────────────────────────────────────
@app.post(
    "/courses/",
    summary="Add one or more courses",
    responses={
        400: {"description": "Duplicate course_id in request or existing data"},
    },
)
def create_courses(courses: List[Course]):
    """Validate and persist a list of courses to `courses.json`."""
    if not courses:
        raise HTTPException(status_code=400, detail="Course list cannot be empty.")

    existing = load_courses()
    existing_ids = {c["course_id"] for c in existing}

    incoming_ids = [c.course_id for c in courses]
    if len(incoming_ids) != len(set(incoming_ids)):
        raise HTTPException(
            status_code=400, detail="Duplicate course_id values in request body."
        )

    duplicates = existing_ids.intersection(incoming_ids)
    if duplicates:
        raise HTTPException(
            status_code=400,
            detail=f"Course(s) already exist: {sorted(duplicates)}",
        )

    existing.extend(course.model_dump() for course in courses)
    save_courses(existing)

    return {"message": f"{len(courses)} course(s) saved successfully.", "courses": courses}


@app.get("/courses/", summary="List all stored courses")
def list_courses():
    return load_courses()
