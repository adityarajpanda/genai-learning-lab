"""
FastAPI endpoint to delete a student record from a Neon (PostgreSQL) database.
"""

import os

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Student Records API - Delete",
    description="Delete student records stored in a Neon PostgreSQL database.",
    version="1.0.0",
)


def get_db_connection():
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="DATABASE_URL environment variable is not configured.",
        )
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def delete_student_by_id(student_id: str) -> bool:
    """Delete the student row matching student_id. Returns True if a row was deleted."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s RETURNING student_id",
                (student_id,),
            )
            deleted = cur.fetchone()
        conn.commit()
        return deleted is not None
    finally:
        conn.close()


@app.delete(
    "/students/{student_id}",
    summary="Delete a student by ID",
    responses={
        404: {"description": "Student not found"},
        500: {"description": "Server / database error"},
    },
)
def remove_student(student_id: str):
    """Delete a single student record by **student_id** (e.g. `STU001`)."""
    try:
        was_deleted = delete_student_by_id(student_id)
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

    if not was_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found.",
        )

    return {"message": f"Student with ID '{student_id}' deleted successfully."}
