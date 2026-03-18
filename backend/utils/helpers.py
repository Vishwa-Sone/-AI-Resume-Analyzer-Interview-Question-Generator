"""
helpers.py
==========
Small reusable utility functions used
across multiple backend files.

Rule: If the same code is needed in more
than one place → put it here.
"""

import uuid
import os
import json


def generate_candidate_id() -> str:
    """
    Generate a unique ID for each candidate.

    Why?
    ChromaDB needs a unique collection name
    per candidate to avoid data mixing.

    Example output: "candidate_a3f8b2c1d4e5"
    """
    return f"candidate_{uuid.uuid4().hex[:12]}"


def save_upload(
    file_bytes:  bytes,
    filename:    str,
    upload_dir:  str = "data/uploads"
) -> str:
    """
    Save uploaded resume file to disk.
    """
    # Use absolute path — fixes Windows path issues
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    abs_upload_dir = os.path.join(base_dir, upload_dir)

    # Check if folder exists before creating
    if not os.path.exists(abs_upload_dir):
        os.makedirs(abs_upload_dir)

    file_path = os.path.join(abs_upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path


def clean_json_response(raw_text: str) -> dict:
    """
    Clean LLM response and parse as JSON.

    Why?
    Gemini sometimes wraps JSON in markdown:
```json
    {"name": "John"}
```
    This function strips those wrappers.

    Example:
        Input  → "```json\n{\"name\": \"John\"}\n```"
        Output → {"name": "John"}
    """
    text = raw_text.strip()

    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())


def is_valid_file(filename: str) -> bool:
    """
    Check if uploaded file is PDF or DOCX.

    Why?
    Security check — only process supported formats.
    Prevents users uploading wrong file types.

    Returns:
        True if valid, False otherwise
    """
    allowed = {"pdf", "docx"}
    ext = filename.lower().split(".")[-1]
    return ext in allowed


def truncate_text(
    text:      str,
    max_chars: int = 8000
) -> str:
    """
    Truncate resume text to avoid token limit errors.

    Why?
    Gemini has a maximum input size.
    Very long resumes could exceed the limit.
    8000 characters covers most resumes fully.

    Returns:
        Truncated text string
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[Text truncated]"