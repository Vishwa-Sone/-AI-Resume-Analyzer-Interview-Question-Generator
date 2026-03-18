"""
schemas.py
==========
Defines the exact shape of data going in
and out of the API using Pydantic models.

Why Pydantic?
- FastAPI uses it to validate data automatically
- If wrong data is sent → FastAPI returns clear error
- Self-documenting — Swagger UI shows exact fields
- Think of it as a contract:
  "This is exactly what I accept and return"
"""

from pydantic import BaseModel
from typing import List, Optional


# ── Sub models ────────────────────────────────────────────────────

class Education(BaseModel):
    degree:    str
    institute: str
    year:      str


class Experience(BaseModel):
    role:        str
    company:     str
    duration:    str
    description: str


class Project(BaseModel):
    name:        str
    tech:        str
    description: str


# ── Main models ───────────────────────────────────────────────────

class ResumeInfo(BaseModel):
    """
    Structured data extracted from resume by Gemini.
    This is what extractor.py returns.
    """
    name:       str
    email:      str
    phone:      str
    skills:     List[str]
    education:  List[Education]
    experience: List[Experience]
    projects:   List[Project]


class AnalyzeResponse(BaseModel):
    """
    Final response returned by /analyze endpoint.
    This is exactly what Streamlit receives.

    extracted_info      → candidate details
    interview_questions → categorized questions
    """
    extracted_info:      dict
    interview_questions: dict


class QuestionRequest(BaseModel):
    """
    Request body for /questions/generate endpoint.
    """
    resume_text:     str
    job_role:        str
    job_description: Optional[str] = ""