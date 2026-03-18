"""
question_gen.py
===============
RAG pipeline that generates categorized interview
questions based on the candidate's resume.

What is RAG?
R = Retrieval  → fetch relevant chunks from ChromaDB
A = Augmented  → add those chunks to the Gemini prompt
G = Generation → Gemini generates questions from context

Why RAG instead of sending the whole resume?
- More targeted questions per category
- Works even for very long resumes
- Questions are grounded in specific resume details
- Faster and cheaper (fewer tokens sent to Gemini)

temperature=0.7 here (not 0 like extractor.py)
Because we want some creativity in questions —
not the exact same questions every time.
"""

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from .embedder import create_temp_vectorstore

load_dotenv()


def generate_questions(
    resume_text:     str,
    job_role:        str,
    job_description: str  = "",
    extracted_info:  dict = None
) -> dict:
    """
    Generate categorized interview questions using RAG.

    Args:
        resume_text     : full plain text of the resume
        job_role        : target job role e.g. "AI ML Engineer"
        job_description : optional job description for
                          more targeted questions
        extracted_info  : structured resume data from extractor.py
                          used to count projects dynamically

    Returns:
        Dictionary with 4 categories:
        {
            "Technical":     [...5 questions],
            "Project-Based": [...1 per project],
            "Behavioral":    [...2 questions],
            "Situational":   [...2 questions]
        }
    """

    # Step 1 — Dynamically calculate project question count
    # 1 question per project, minimum 2, maximum 5
    project_count = 2   # default if no info available
    project_names = ""

    if extracted_info:
        projects = extracted_info.get("projects", [])

        # Count — min 2, max 5
        project_count = max(2, min(len(projects), 5))

        # Build project list string for the prompt
        # So Gemini knows exactly which projects to cover
        project_names = "\n".join([
            f"- {p['name']} (Tech: {p['tech']})"
            for p in projects
        ])

    # Step 2 — Define question count per category
    category_counts = {
        "Technical":     5,
        "Project-Based": project_count,  # dynamic based on projects
        "Behavioral":    2,
        "Situational":   2,
    }

    # Step 3 — Build temporary vector store from resume
    # Converts resume text to vectors in memory
    vectorstore = create_temp_vectorstore(resume_text)

    # Step 4 — Create retriever
    # k=4 means retrieve top 4 most relevant chunks
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # Step 5 — Initialize Gemini
    # temperature=0.7 for some creativity in questions
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

    # Step 6 — Define search queries for each category
    # Each query finds the most relevant resume section
    category_queries = {
        "Technical":     "technical skills programming languages frameworks tools",
        "Project-Based": "projects built developed implemented",
        "Behavioral":    "experience work achievements teamwork",
        "Situational":   "challenges problems solved leadership decisions",
    }

    # Step 7 — Define prompt template
    prompt_template = PromptTemplate(
        input_variables=[
            "category",
            "count",
            "context",
            "job_role",
            "job_description",
            "project_names",
        ],
        template="""
You are an expert technical interviewer.

Generate {count} {category} interview questions for a
candidate applying for the role of {job_role}.

Job Description:
{job_description}

Candidate's Projects:
{project_names}

Relevant information from the candidate's resume:
{context}

Rules:
- Questions must be specific to THIS candidate's background
- For Project-Based questions, cover ALL projects listed above
  — generate at least one question per project
- Reference their actual skills, projects, or experience
- Make questions clear and professional
- Return ONLY a valid JSON array of question strings
- No explanation, no markdown, just the JSON array

Example format:
["Question 1?", "Question 2?", "Question 3?"]

Generate {count} {category} questions now:
"""
    )

    # Step 8 — Generate questions for each category
    all_questions = {}

    for category, query in category_queries.items():

        # Retrieve relevant resume chunks for this category
        relevant_docs = retriever.invoke(query)

        # Join all retrieved chunks into one context string
        context = "\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        # Format the prompt with actual values
        formatted_prompt = prompt_template.format(
            category=category,
            count=category_counts[category],
            context=context,
            job_role=job_role,
            job_description=job_description or "Not specified",
            project_names=project_names or "Not specified"
        )

        # Send to Gemini
        response = llm.invoke(formatted_prompt)
        raw = response.content.strip()

        # Clean response — remove markdown if Gemini adds it
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        # Parse JSON array into Python list
        questions = json.loads(raw.strip())
        all_questions[category] = questions

        print(f"✅ {category} questions generated "
              f"({len(questions)} questions)")

    return all_questions