"""
FastAPI endpoint to update (partially or fully) a student record in a Neon
(PostgreSQL) database.
"""

import os
from datetime import date
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Student Records API - Update",
    description="Update student records stored in a Neon PostgreSQL database.",
    version="1.0.0",
)


# ── Request model ────────────────────────────────────────────────────
class StudentUpdate(BaseModel):
    """All fields optional so callers can send only the fields they want to change."""

    name: Optional[str] = None
    email: Optional[str] = None
    grade: Optional[str] = None
    enrollment_date: Optional[date] = None


def get_db_connection():
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="DATABASE_URL environment variable is not configured.",
        )
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def update_student_by_id(student_id: str, updates: dict) -> Optional[dict]:
    """Update only the provided fields for a student. Returns the updated row, or None if not found."""
    set_clause = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values()) + [student_id]

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE students
                SET    {set_clause}
                WHERE  student_id = %s
                RETURNING student_id, name, email, grade, enrollment_date
                """,
                values,
            )
            updated = cur.fetchone()
        conn.commit()
        return updated
    finally:
        conn.close()


@app.put(
    "/students/{student_id}",
    summary="Update a student by ID (partial updates supported)",
    responses={
        404: {"description": "Student not found"},
        400: {"description": "No fields provided to update"},
        500: {"description": "Server / database error"},
    },
)
def update_student(student_id: str, student_update: StudentUpdate):
    """Update a student record. Only fields present in the request body are changed."""
    updates = student_update.model_dump(exclude_unset=True, exclude_none=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided to update.",
        )

    try:
        updated_student = update_student_by_id(student_id, updates)
    except HTTPException:
        raise
    except psycopg2.OperationalError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to the database: {exc}",
        )
    except psycopg2.Error as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {exc}",
        )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found.",
        )

    return updated_student
