"""
extractor.py
============
Sends resume text to Gemini and gets back
structured information as a Python dictionary.

Why LangChain instead of calling Gemini API directly?
- PromptTemplate makes it easy to format prompts cleanly
- Handles API errors and retries automatically
- Easy to switch to a different LLM later if needed

Why temperature=0?
Temperature controls how creative/random the output is.
0 = fully deterministic — we want consistent, factual
extraction, not creative writing.
"""

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load GOOGLE_API_KEY from .env file
load_dotenv()


def extract_info(resume_text: str) -> dict:
    """
    Extract structured information from resume text using Gemini.

    Args:
        resume_text : plain text extracted from the resume

    Returns:
        Dictionary with keys:
        name, email, phone, skills,
        education, experience, projects
    """

    # Step 1 — Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0        # no randomness — we want facts only
    )

    # Step 2 — Define the prompt template
    # {resume_text} is a placeholder — gets replaced with actual text
    # We tell Gemini exactly what JSON format we want back
    prompt_template = PromptTemplate(
        input_variables=["resume_text"],
        template="""
You are an expert resume parser.
Extract information from the resume below and return
it as valid JSON only.
Do not include any explanation or markdown formatting.

Resume Text:
{resume_text}

Return exactly this JSON structure:
{{
    "name": "full name of candidate",
    "email": "email address",
    "phone": "phone number",
    "skills": ["skill1", "skill2", "skill3"],
    "education": [
        {{
            "degree": "degree name",
            "institute": "institution name",
            "year": "graduation year"
        }}
    ],
    "experience": [
        {{
            "role": "job title",
            "company": "company name",
            "duration": "duration e.g. 6 months",
            "description": "what they did"
        }}
    ],
    "projects": [
        {{
            "name": "project name",
            "tech": "technologies used",
            "description": "what the project does"
        }}
    ]
}}

Important rules:
- If a field is not found, use empty string "" or empty list []
- skills must be a flat list of strings
- Return only valid JSON, absolutely nothing else
"""
    )

    # Step 3 — Fill in the placeholder with actual resume text
    formatted_prompt = prompt_template.format(
        resume_text=resume_text
    )

    # Step 4 — Send to Gemini and get response
    response = llm.invoke(formatted_prompt)

    # Step 5 — Clean and parse the response
    # response.content is the raw text Gemini returned
    raw_text = response.content.strip()

    # Sometimes Gemini wraps JSON in ```json ... ```
    # We need to remove those before parsing
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    # Convert JSON string to Python dictionary
    extracted = json.loads(raw_text.strip())

    return extracted