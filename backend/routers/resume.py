"""
resume.py — Router
==================
Handles the resume upload endpoint.

Why separate router files?
- Keeps main.py clean
- Each router handles one feature area
- Easy to add new routes later

prefix="/resume" means all routes here
start with /resume
→ /resume/upload
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.parser import parse_resume
from ..utils.helpers import is_valid_file, save_upload

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload resume and extract text from it.

    Endpoint : POST /resume/upload
    Input    : PDF or DOCX file
    Output   : extracted text + filename
    """

    # Validate file type
    if not is_valid_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # Read file bytes
    file_bytes = await file.read()

    # Save to disk for reference
    save_upload(file_bytes, file.filename)

    # Extract text
    text = parse_resume(file_bytes, file.filename)

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text. File may be a scanned image."
        )

    return {
        "filename":       file.filename,
        "text_length":    len(text),
        "extracted_text": text
    }
    