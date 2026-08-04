"""
FastAPI endpoint to retrieve student records from a Neon (PostgreSQL) database.
"""

import os
from datetime import date
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

# ── Load environment variables ───────────────────────────────────────
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ── FastAPI app ──────────────────────────────────────────────────────
app = FastAPI(
    title="Student Records API",
    description="Retrieve student records stored in a Neon PostgreSQL database.",
    version="1.0.0",
)


# ── Response model ───────────────────────────────────────────────────
class StudentResponse(BaseModel):
    student_id: str
    name: str
    email: Optional[str] = None
    grade: Optional[str] = None
    enrollment_date: Optional[date] = None

    model_config = {"json_schema_extra": {
        "examples": [{
            "student_id": "STU001",
            "name": "Aditya Sharma",
            "email": "aditya@example.com",
            "grade": "A",
            "enrollment_date": "2025-08-01",
        }]
    }}


# ── Database helper ──────────────────────────────────────────────────
def get_db_connection():
    """Return a new psycopg2 connection using the Neon DATABASE_URL.

    Neon connection strings already include `sslmode=require`, so no
    extra SSL configuration is needed here.
    """
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="DATABASE_URL environment variable is not configured.",
        )
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


# ── Core retrieval function ──────────────────────────────────────────
def get_student_by_id(student_id: str) -> Optional[dict]:
    """Query the students table and return a single record or None."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT student_id, name, email, grade, enrollment_date
                FROM   students
                WHERE  student_id = %s
                """,
                (student_id,),
            )
            return cur.fetchone()
    finally:
        conn.close()


# ── API endpoint ─────────────────────────────────────────────────────
@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by ID",
    responses={
        404: {"description": "Student not found"},
        500: {"description": "Server / database error"},
    },
)
def read_student(student_id: str):
    """Retrieve a single student record by **student_id** (e.g. `STU001`)."""
    try:
        student = get_student_by_id(student_id)
    except HTTPException:
        raise  # re-raise the 500 from missing DATABASE_URL
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

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found.",
        )

    return student