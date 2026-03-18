import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
import requests
import streamlit as st
from shared import (inject_css, topbar, navbar, breadcrumb, section_title,
                    step_bar, card_heading, info_note)

st.set_page_config(
    page_title="Upload Resume — ResumeAI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()
topbar()
navbar("upload")

# ── SESSION DEFAULTS ──────────────────────────────────────────────────────────
for key, val in [
    ("uploaded_file_name", None),
    ("job_role",           ""),
    ("job_description",    ""),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
breadcrumb(["Home", "Upload Resume"])
section_title("Upload Resume")
st.markdown("""
<p style="color:#6b6b7b;font-size:.93rem;margin:.4rem 0 1.8rem;line-height:1.7">
  Upload a candidate's resume and provide the target job role.
  Accepted formats: <strong style="color:#1c2b4a">PDF</strong>
  and <strong style="color:#1c2b4a">DOCX</strong>, up to 10 MB.
</p>
""", unsafe_allow_html=True)

step_bar(1)

# ── RESUME FILE CARD ──────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
            border-top:3px solid #b5451b;padding:1.6rem 2rem 1.2rem;
            margin-bottom:1.2rem;box-shadow:0 1px 4px rgba(28,43,74,.06)">
  <p style="font-family:'Lora',serif;font-size:.93rem;font-weight:700;
            color:#1c2b4a;margin:0 0 1rem">Resume File</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX file (max 10 MB)",
    type=["pdf", "docx"],
)

if uploaded_file:
    size_kb = len(uploaded_file.getvalue()) / 1024
    st.markdown(f"""
    <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:4px;
                padding:.7rem 1rem;display:flex;align-items:center;
                gap:.8rem;margin-top:.9rem">
      <span style="color:#16a34a;font-size:1.1rem;flex-shrink:0">✔</span>
      <div>
        <p style="margin:0;font-size:.87rem;font-weight:700;color:#15803d">
          {uploaded_file.name}
        </p>
        <p style="margin:0;font-size:.76rem;color:#6b6b7b">{size_kb:.1f} KB</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── JOB DETAILS CARD ──────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
            border-top:3px solid #c9973a;padding:1.6rem 2rem 1rem;
            margin-top:1.2rem;margin-bottom:1.2rem;
            box-shadow:0 1px 4px rgba(28,43,74,.06)">
  <p style="font-family:'Lora',serif;font-size:.93rem;font-weight:700;
            color:#1c2b4a;margin:0 0 1rem">Job Details</p>
</div>
""", unsafe_allow_html=True)

job_role = st.text_input(
    "Job Role *",
    placeholder="e.g. Python Backend Developer, Data Analyst, ML Engineer",
    value=st.session_state.job_role,
)
job_description = st.text_area(
    "Job Description (optional — improves question quality)",
    placeholder="Paste job requirements or responsibilities here...",
    height=130,
    value=st.session_state.job_description,
)

# ── TIP NOTE ──────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
info_note(
    "<strong>Tip:</strong> A job description helps generate more targeted "
    "interview questions. Even a few bullet points make a difference."
)

# ── ANALYZE BUTTON ────────────────────────────────────────────────────────────
btn_col, _ = st.columns([1, 2])
with btn_col:
    analyze_clicked = st.button("Analyze Resume →", key="analyze_btn")

if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume file before proceeding.")
    elif not job_role.strip():
        st.error("Job role is required. Please enter the target job title.")
    else:
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.job_role           = job_role
        st.session_state.job_description    = job_description
        st.session_state.resume_bytes       = uploaded_file.getvalue()

        # ── Real API call to FastAPI backend ──────────────────────────────────
        try:
            with st.spinner("⏳ Analyzing resume... this may take 30-60 seconds"):
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    },
                    data={
                        "job_role":        job_role,
                        "job_description": job_description
                    },
                    timeout=120   # 2 minutes for Gemini to respond
                )

            if response.status_code == 200:
                result = response.json()
                st.session_state.extracted_info      = result["extracted_info"]
                st.session_state.interview_questions = result["interview_questions"]
                st.session_state.analysis_done       = True
                st.success("✔ Analysis complete — redirecting to results...")
                time.sleep(0.8)
                st.switch_page("pages/Analysis_Result.py")
            else:
                st.error(
                    f"Backend error {response.status_code}: {response.text}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Cannot connect to backend. "
                "Make sure FastAPI is running on port 8000.\n\n"
                "Run this in a separate terminal:\n"
                "uvicorn backend.main:app --reload --port 8000"
            )
        except requests.exceptions.Timeout:
            st.error(
                "❌ Request timed out. "
                "Gemini is taking too long. Please try again."
            )
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")