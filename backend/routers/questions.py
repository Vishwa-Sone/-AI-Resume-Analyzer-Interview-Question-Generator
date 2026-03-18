"""
questions.py — Router
=====================
Handles interview question generation endpoint.

This is a standalone endpoint — useful when you
want to regenerate questions for an already
processed resume without re-uploading it.
"""

from fastapi import APIRouter, HTTPException
from ..services.question_gen import generate_questions
from ..models.schemas import QuestionRequest

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/generate")
async def generate_interview_questions(
    request: QuestionRequest
):
    """
    Generate interview questions from resume text.

    Endpoint : POST /questions/generate
    Input    : resume_text, job_role, job_description
    Output   : categorized interview questions
    """

    if not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    questions = generate_questions(
        resume_text=request.resume_text,
        job_role=request.job_role,
        job_description=request.job_description
    )

    return {"interview_questions": questions}


