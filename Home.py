import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from shared import (inject_css, topbar, navbar, divider_label)

st.set_page_config(
    page_title="ResumeAI — Resume Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()
topbar()
navbar("home")

#  HERO 
st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
col_hero, col_card = st.columns([1.55, 1], gap="large")

with col_hero:
    # Eyebrow
    st.markdown("""
    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:1.2rem">
      <div style="width:26px;height:2px;background:#c9973a;flex-shrink:0"></div>
      <span style="font-size:.72rem;font-weight:700;letter-spacing:.12em;
                   color:#c9973a;text-transform:uppercase;
                   font-family:'Nunito Sans',sans-serif">
        Recruitment Intelligence Platform
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Heading
    st.markdown("""
    <h1 style="font-size:2.4rem;font-weight:700;line-height:1.25;
               margin:0 0 1rem;color:#1c2b4a;font-family:'Lora',serif">
      Analyze Resumes &amp;<br>
      <em style="color:#b5451b;font-style:italic">
        Generate Interview Questions
      </em>
    </h1>
    """, unsafe_allow_html=True)

    # Subtitle
    st.markdown("""
    <p style="font-size:.98rem;color:#6b6b7b;line-height:1.85;
              margin:0 0 1.8rem;max-width:500px;font-weight:400">
      Upload a PDF or DOCX resume, specify the target job role, and receive a
      comprehensive structured analysis alongside categorized interview questions —
      powered by a Gemini LLM and RAG pipeline.
    </p>
    """, unsafe_allow_html=True)

    # Feature badges
    badges = [
        ("#fdf0ec", "#e8bfb0", "#b5451b", "✦ Resume Parsing"),
        ("#f0f4fd", "#bfcfee", "#1c4db5", "✦ Skill Extraction"),
        ("#fdf8ee", "#e8d9a0", "#a07820", "✦ RAG Pipeline"),
        ("#f0fdf4", "#a0dbb5", "#186a3b", "✦ Interview Q&amp;A"),
    ]
    badge_html = '<div style="display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:2rem">'
    for bg, bd, fg, txt in badges:
        badge_html += (
            f'<span style="background:{bg};border:1px solid {bd};color:{fg};'
            f'border-radius:3px;padding:.25rem .8rem;font-size:.76rem;'
            f'font-weight:700;letter-spacing:.03em">{txt}</span>'
        )
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

    # CTA button
    _, btn_col, _ = st.columns([.05, 1.2, 1.2])
    with btn_col:
        if st.button("Begin Analysis →", key="hero_btn"):
            st.switch_page("pages/Upload_Resume.py")

#  WHAT YOU RECEIVE CARD 
with col_card:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                border-top:3px solid #b5451b;padding:1.6rem 1.6rem .4rem;
                margin-top:.4rem;box-shadow:0 1px 8px rgba(28,43,74,.08)">
      <p style="font-family:'Lora',serif;font-size:.97rem;font-weight:600;
                color:#1c2b4a;margin:0 0 1.1rem;padding-bottom:.7rem;
                border-bottom:1px solid #e2d9cc">
        What you receive
      </p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("#fdf0ec","#e8bfb0","📄","Structured Resume Data",
         "Name, contact, skills, education, experience, projects"),
        ("#f0f4fd","#bfcfee","🔧","Technical Interview Questions",
         "Based on candidate's actual skills and tech stack"),
        ("#fdf8ee","#e8d9a0","🚀","Project-Based Questions",
         "Tailored to the candidate's listed projects"),
        ("#f0fdf4","#a0dbb5","🧠","Behavioral & Situational",
         "Role-specific soft skill assessment questions"),
    ]
    for bg, bd, icon, title, desc in features:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                    padding:.85rem 1rem;margin-bottom:.6rem;
                    display:flex;gap:.85rem;align-items:flex-start">
          <div style="background:{bg};border:1px solid {bd};border-radius:50%;
                      width:30px;height:30px;display:flex;align-items:center;
                      justify-content:center;flex-shrink:0;font-size:14px">
            {icon}
          </div>
          <div>
            <p style="font-size:.86rem;font-weight:700;color:#1c2b4a;margin:0">
              {title}
            </p>
            <p style="font-size:.78rem;color:#6b6b7b;margin:.1rem 0 0;line-height:1.5">
              {desc}
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:.73rem;color:#c9973a;font-weight:700;
              letter-spacing:.06em;text-transform:uppercase;
              margin:.4rem 0 0;padding-top:.7rem;border-top:1px solid #e2d9cc">
      Supported formats: PDF &nbsp;·&nbsp; DOCX
    </p>
    """, unsafe_allow_html=True)

#  HOW IT WORKS 
divider_label("How It Works")

steps = [
    ("I",   "#b5451b","#fdf0ec","#e8bfb0","Upload Resume",
     "Upload a PDF or DOCX candidate resume file."),
    ("II",  "#1c4db5","#f0f4fd","#bfcfee","Enter Job Role",
     "Specify the target position for tailored analysis."),
    ("III", "#a07820","#fdf8ee","#e8d9a0","AI Processes",
     "LLM extracts structured data via the RAG pipeline."),
    ("IV",  "#186a3b","#f0fdf4","#a0dbb5","View & Export",
     "Review the analysis and download interview questions."),
]

cols = st.columns(4, gap="medium")
for col, (num, color, bg, bd, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                    padding:1.3rem;border-top:3px solid {color};
                    box-shadow:0 1px 4px rgba(28,43,74,.05)">
          <div style="background:{bg};border:1px solid {bd};color:{color};
                      font-family:'Lora',serif;font-weight:700;font-size:.8rem;
                      display:inline-block;padding:.2rem .65rem;border-radius:3px;
                      margin-bottom:.8rem">Step {num}</div>
          <p style="font-family:'Lora',serif;font-size:.9rem;font-weight:600;
                    color:#1c2b4a;margin:0 0 .35rem">{title}</p>
          <p style="font-size:.8rem;color:#6b6b7b;margin:0;line-height:1.65">
            {desc}
          </p>
        </div>
        """, unsafe_allow_html=True)

#  CTA BANNER 
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#1c2b4a;border-radius:4px;padding:2rem 2.5rem;
            display:flex;align-items:center;justify-content:space-between;
            flex-wrap:wrap;gap:1rem">
  <div>
    <p style="font-family:'Lora',serif;font-size:1.1rem;font-weight:700;
              margin:0 0 .25rem;color:#fff">Ready to analyze a resume?</p>
    <p style="font-size:.84rem;color:#a0b0cc;margin:0">
      Upload a resume file and receive a complete analysis in under a minute.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:.8rem'></div>", unsafe_allow_html=True)
_, cta_col, _ = st.columns([2.5, 1.4, 2.5])
with cta_col:
    if st.button("Get Started →", key="cta_btn"):
        st.switch_page("pages/Upload_Resume.py")