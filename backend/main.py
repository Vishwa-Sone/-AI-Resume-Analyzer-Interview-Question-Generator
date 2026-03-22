

import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .services.parser import parse_resume
from .services.extractor import extract_info
from .services.question_gen import generate_questions
from .models.schemas import AnalyzeResponse
from .utils.helpers import is_valid_file, truncate_text, save_upload
from .routers import resume, questions
load_dotenv()

app = FastAPI(
    title="ResumeAI Backend",
    description="AI-powered resume analyzer and interview question generator",
    version="1.0.0"
)

# CORS Middleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers 

app.include_router(resume.router)
app.include_router(questions.router)


#  Health Check
@app.get("/")
def health_check():
    """
    Quick check to confirm API is running.
    Visit http://localhost:8000 to verify.
    """
    return {
        "status":  "running",
        "message": "ResumeAI backend is live!"
    }


# ── MAIN ENDPOINT 
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    file:            UploadFile = File(...),
    job_role:        str        = Form(...),
    job_description: str        = Form("")
):
   

    # Step 1 — Validate file type
    if not is_valid_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # Step 2 — Read file bytes
    file_bytes = await file.read()

    # Step 3 — Save file to disk
    save_upload(file_bytes, file.filename)

    # Step 4 — Parse text from file
    try:
        resume_text = parse_resume(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Failed to parse resume: {str(e)}"
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text found. File may be a scanned image."
        )

    #  Truncate if too long
    resume_text = truncate_text(resume_text, max_chars=8000)

    # —Extract structured info using Gemini
    try:
        extracted_info = extract_info(resume_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract resume info: {str(e)}"
        )


    time.sleep(5)

    # Step 8 — Generate interview questions using RAG
    try:
        interview_questions = generate_questions(
            resume_text=resume_text,
            job_role=job_role,
            job_description=job_description,
            extracted_info=extracted_info
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate questions: {str(e)}"
        )

    # Step 9 — Return everything to Streamlit
    return AnalyzeResponse(
        extracted_info=extracted_info,
        interview_questions=interview_questions
    )