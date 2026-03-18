# ResumeAI — Streamlit Frontend

Classic professional UI built with Streamlit, matching the React version interface.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Opens at: http://localhost:8501

## Project Structure

```
resume-ai-st/
├── shared.py                  # CSS + all reusable components + mock data
├── Home.py                    # Landing page
├── requirements.txt
└── pages/
    ├── Upload_Resume.py       # File upload + job details
    ├── Analysis_Result.py     # Extracted resume info
    └── Interview_Questions.py # Q&A accordion + download
```

## Connect to FastAPI Backend

In `pages/Upload_Resume.py`, uncomment the `requests.post()` block
and remove the mock data block below it:

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    files={"file": (uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type)},
    data={"job_role": job_role, "job_description": job_description},
    timeout=60,
)
result = response.json()
st.session_state.extracted_info      = result["extracted_info"]
st.session_state.interview_questions = result["interview_questions"]
```

## Run With Backend

```bash
# Terminal 1 — FastAPI
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Streamlit
streamlit run Home.py
```
