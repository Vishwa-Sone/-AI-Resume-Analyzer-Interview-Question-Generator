

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

    project_count = 2   
    project_names = ""

    if extracted_info:
        projects = extracted_info.get("projects", [])
        project_count = max(2, min(len(projects), 5))
        project_names = "\n".join([
            f"- {p['name']} (Tech: {p['tech']})"
            for p in projects
        ])

    
    category_counts = {
        "Technical":     5,
        "Project-Based": project_count,  
        "Behavioral":    2,
        "Situational":   2,
    }

    vectorstore = create_temp_vectorstore(resume_text)
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

   
    category_queries = {
        "Technical":     "technical skills programming languages frameworks tools",
        "Project-Based": "projects built developed implemented",
        "Behavioral":    "experience work achievements teamwork",
        "Situational":   "challenges problems solved leadership decisions",
    }

   
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

   
    all_questions = {}

    for category, query in category_queries.items():
        relevant_docs = retriever.invoke(query)

        context = "\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        formatted_prompt = prompt_template.format(
            category=category,
            count=category_counts[category],
            context=context,
            job_role=job_role,
            job_description=job_description or "Not specified",
            project_names=project_names or "Not specified"
        )

       
        response = llm.invoke(formatted_prompt)
        raw = response.content.strip()

        
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

       
        questions = json.loads(raw.strip())
        all_questions[category] = questions

        print(f" {category} questions generated "
              f"({len(questions)} questions)")

    return all_questions