

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


def extract_info(resume_text: str) -> dict:
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0       
    )
    
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

    formatted_prompt = prompt_template.format(
        resume_text=resume_text
    )

    
    response = llm.invoke(formatted_prompt)
    raw_text = response.content.strip()
    if raw_text.starswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    extracted = json.loads(raw_text.strip())

    return extracted