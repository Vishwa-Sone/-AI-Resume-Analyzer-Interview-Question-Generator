"""
shared.py — ResumeAI
====================
Single source of truth for all CSS, layout components, and helpers.
Import and call these functions at the top of every page.

Usage:
    from shared import inject_css, topbar, navbar, ...
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Nunito+Sans:wght@300;400;600;700&display=swap');

/* ── Design tokens ── */
:root {
    --bg:         #faf8f5;
    --white:      #ffffff;
    --cream:      #f5f0e8;
    --border:     #e2d9cc;
    --accent:     #b5451b;
    --accent-dk:  #8f3515;
    --accent-lt:  #fdf0ec;
    --navy:       #1c2b4a;
    --gold:       #c9973a;
    --text:       #1c2b4a;
    --muted:      #6b6b7b;
    --green:      #16a34a;
    --radius:     4px;
    --shadow-sm:  0 1px 4px rgba(28,43,74,0.07);
    --shadow:     0 4px 16px rgba(28,43,74,0.10);
}

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"],
[data-testid="stSidebar"] { display: none !important; }

[data-testid="block-container"] {
    padding: 0 2.5rem 5rem !important;
    max-width: 1100px !important;
    margin: auto !important;
}

h1, h2, h3, h4 {
    font-family: 'Lora', serif !important;
    color: var(--navy) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    padding: .58rem 1.7rem !important;
    width: 100% !important;
    letter-spacing: .03em !important;
    transition: background .18s !important;
    box-shadow: var(--shadow-sm) !important;
    cursor: pointer !important;
}
.stButton > button:hover { background: var(--accent-dk) !important; }

/* ── Ghost nav buttons ── */
.nav-btn .stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
    padding: .3rem .9rem !important;
    width: auto !important;
    box-shadow: none !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
}
.nav-btn .stButton > button:hover {
    background: var(--cream) !important;
    border-color: var(--gold) !important;
    color: var(--accent) !important;
}

/* ── Active nav button ── */
.nav-btn-active .stButton > button {
    background: var(--accent-lt) !important;
    border: 1px solid #e8bfb0 !important;
    color: var(--accent) !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
    padding: .3rem .9rem !important;
    width: auto !important;
    box-shadow: none !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
}

/* ── Outline button ── */
.outline-btn .stButton > button {
    background: var(--white) !important;
    color: var(--accent) !important;
    border: 1.5px solid var(--accent) !important;
    box-shadow: none !important;
}
.outline-btn .stButton > button:hover {
    background: var(--accent-lt) !important;
}

/* ── Navy button ── */
.navy-btn .stButton > button {
    background: var(--navy) !important;
    color: #fff !important;
}
.navy-btn .stButton > button:hover { background: #0f1d38 !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: var(--navy) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    padding: .58rem 1.7rem !important;
    width: 100% !important;
    letter-spacing: .03em !important;
    transition: background .18s !important;
    box-shadow: var(--shadow-sm) !important;
    cursor: pointer !important;
}
[data-testid="stDownloadButton"] > button:hover { background: #0f1d38 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--white) !important;
    border: 2px dashed #c9b99a !important;
    border-radius: var(--radius) !important;
    padding: .9rem !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {
    background: var(--white) !important;
    color: var(--accent) !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: var(--radius) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: .82rem !important;
    padding: .32rem 1rem !important;
    width: auto !important;
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    box-shadow: none !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover {
    background: var(--accent-lt) !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: var(--white) !important;
    border: none !important;
    padding: .4rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--muted) !important;
    font-size: .83rem !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: .92rem !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(181,69,27,.1) !important;
}

/* ── Labels ── */
label, [data-testid="stWidgetLabel"] p {
    color: var(--navy) !important;
    font-size: .86rem !important;
    font-weight: 700 !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

/* ── Expander — fixed black background issue ── */
[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: .5rem !important;
    box-shadow: 0 1px 3px rgba(28,43,74,.04) !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: .88rem !important;
    color: var(--navy) !important;
    font-weight: 600 !important;
    padding: .65rem .9rem !important;
    background: var(--white) !important;
}
[data-testid="stExpander"] summary:hover {
    background: #faf8f5 !important;
}
[data-testid="stExpander"] summary:focus {
    background: var(--white) !important;
    outline: none !important;
}
[data-testid="stExpander"] > div {
    background: var(--white) !important;
    color: var(--navy) !important;
}
[data-testid="stExpander"] > div > div {
    background: var(--white) !important;
    color: var(--navy) !important;
}
[data-testid="stExpander"][open] {
    background: var(--white) !important;
}
[data-testid="stExpander"][open] summary {
    background: var(--white) !important;
    color: var(--navy) !important;
    border-bottom: 1px solid var(--border) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: var(--border) !important;
    border-radius: 2px !important;
    height: 4px !important;
}
[data-testid="stProgress"] > div > div > div {
    background: var(--accent) !important;
    border-radius: 2px !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: .88rem !important;
}

/* ── HR ── */
hr { border: none !important; border-top: 1px solid var(--border) !important; }

/* ── Button row alignment ── */
.outline-btn .stButton > button,
.stButton > button {
    vertical-align: middle !important;
}
.outline-btn {
    display: flex !important;
    align-items: stretch !important;
}
.outline-btn .stButton {
    width: 100% !important;
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
#  INJECT CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    """Call once at the top of every page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TOP BAR  — dark navy announcement strip
# ─────────────────────────────────────────────────────────────────────────────
def topbar():
    st.markdown("""
    <div style="background:#1c2b4a;padding:.45rem 2.5rem;
                margin:-1rem -2.5rem 0;text-align:center">
      <span style="font-size:.72rem;color:#a0b0cc;letter-spacing:.08em;
                   font-family:'Nunito Sans',sans-serif">
        AI-POWERED RECRUITMENT ASSISTANT &nbsp;·&nbsp; LLM + RAG PIPELINE
      </span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  NAVBAR  — white bar with logo and page links
# ─────────────────────────────────────────────────────────────────────────────
def navbar(current_page):
    """
    current_page: 'home' | 'upload' | 'analysis' | 'questions'
    """
    st.markdown("""
    <div style="background:#fff;border-bottom:2px solid #e2d9cc;
                padding:.9rem 2.5rem;margin:0 -2.5rem;
                display:flex;align-items:center;justify-content:space-between">
      <div style="display:flex;align-items:center;gap:.6rem">
        <span style="font-size:1.3rem">📋</span>
        <span style="font-family:'Lora',serif;font-weight:700;
                     font-size:1.15rem;color:#1c2b4a">ResumeAI</span>
        <span style="font-size:.68rem;color:#c9973a;font-weight:700;
                     letter-spacing:.1em;margin-left:.3rem;
                     font-family:'Nunito Sans',sans-serif">PROFESSIONAL</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    _, c1, c2, _ = st.columns([7, .75, .85, .1])
    with c1:
        cls = "nav-btn-active" if current_page == "home" else "nav-btn"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("Home", key="nav_home"):
            st.switch_page("Home.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        cls = "nav-btn-active" if current_page == "upload" else "nav-btn"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("Upload", key="nav_upload"):
            st.switch_page("pages/Upload_Resume.py")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:.5rem 0 0'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  BREADCRUMB  — Home › Upload › Analysis Results
# ─────────────────────────────────────────────────────────────────────────────
def breadcrumb(crumbs: list):
    parts = []
    for i, c in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span style="color:#b5451b;font-weight:700">{c}</span>')
        else:
            parts.append(f'<span style="color:#6b6b7b">{c}</span>')
    html = ' <span style="color:#c0b8ad">&nbsp;›&nbsp;</span> '.join(parts)
    st.markdown(
        f'<p style="font-size:.77rem;margin:1.6rem 0 1.2rem">{html}</p>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION TITLE  — red left-bar + big heading
# ─────────────────────────────────────────────────────────────────────────────
def section_title(text: str):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.4rem">
      <div style="width:4px;height:32px;background:#b5451b;
                  border-radius:2px;flex-shrink:0"></div>
      <h1 style="font-size:1.65rem;font-weight:700;margin:0;
                 font-family:'Lora',serif;color:#1c2b4a">{text}</h1>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  STEP BAR  — 1 → 2 → 3 tracker
#  Pure Streamlit columns — no HTML string joining at all
# ─────────────────────────────────────────────────────────────────────────────
def step_bar(step: int):
    c1_bg = "#16a34a" if 1 < step else ("#b5451b" if 1 == step else "#e2d9cc")
    c1_fg = "#fff"    if step >= 1  else "#a0a0b0"
    c1_lb = "✔"       if 1 < step  else "1"

    l1_bg = "#16a34a" if 1 < step else ("#b5451b" if 1 == step else "#e2d9cc")

    c2_bg = "#16a34a" if 2 < step else ("#b5451b" if 2 == step else "#e2d9cc")
    c2_fg = "#fff"    if step >= 2  else "#a0a0b0"
    c2_lb = "✔"       if 2 < step  else "2"

    l2_bg = "#16a34a" if 2 < step else ("#b5451b" if 2 == step else "#e2d9cc")

    c3_bg = "#16a34a" if 3 < step else ("#b5451b" if 3 == step else "#e2d9cc")
    c3_fg = "#fff"    if step >= 3  else "#a0a0b0"
    c3_lb = "✔"       if 3 < step  else "3"

    label_text = "Step 3 of 3 — Complete" if step == 3 else f"Step {step} of 3"

    col1, lcol1, col2, lcol2, col3, label_col = st.columns(
        [.15, .8, .15, .8, .15, 2.5]
    )

    with col1:
        st.markdown(
            f'<div style="background:{c1_bg};color:{c1_fg};border-radius:50%;'
            f'width:26px;height:26px;display:flex;align-items:center;'
            f'justify-content:center;font-size:.72rem;font-weight:700">'
            f'{c1_lb}</div>',
            unsafe_allow_html=True
        )
    with lcol1:
        st.markdown(
            f'<div style="height:2px;background:{l1_bg};margin-top:12px"></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div style="background:{c2_bg};color:{c2_fg};border-radius:50%;'
            f'width:26px;height:26px;display:flex;align-items:center;'
            f'justify-content:center;font-size:.72rem;font-weight:700">'
            f'{c2_lb}</div>',
            unsafe_allow_html=True
        )
    with lcol2:
        st.markdown(
            f'<div style="height:2px;background:{l2_bg};margin-top:12px"></div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f'<div style="background:{c3_bg};color:{c3_fg};border-radius:50%;'
            f'width:26px;height:26px;display:flex;align-items:center;'
            f'justify-content:center;font-size:.72rem;font-weight:700">'
            f'{c3_lb}</div>',
            unsafe_allow_html=True
        )
    with label_col:
        st.markdown(
            f'<p style="font-size:.76rem;color:#6b6b7b;margin:4px 0 0 6px;'
            f'font-family:\'Nunito Sans\',sans-serif">{label_text}</p>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  DIVIDER LABEL  —  ──── Export & Actions ────
# ─────────────────────────────────────────────────────────────────────────────
def divider_label(label: str = None):
    inner = (
        f'<span style="font-family:\'Lora\',serif;font-size:.82rem;'
        f'font-style:italic;color:#c9973a;white-space:nowrap">{label}</span>'
    ) if label else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1rem;margin:2.5rem 0 2rem">
      <div style="flex:1;height:1px;background:#e2d9cc"></div>
      {inner}
      <div style="flex:1;height:1px;background:#e2d9cc"></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  INFO NOTE  — gold left-border tip box
# ─────────────────────────────────────────────────────────────────────────────
def info_note(text: str):
    st.markdown(f"""
    <div style="background:#fdf8ee;border-left:3px solid #c9973a;
                padding:.72rem 1rem;margin-bottom:1.8rem;
                border-radius:0 4px 4px 0">
      <p style="margin:0;font-size:.81rem;color:#7a5c10;line-height:1.6">
        {text}
      </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  CARD HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def card_open(top_color: str = None, padding: str = "1.5rem 2rem",
              margin_bottom: str = "1.2rem"):
    border_top = f"border-top:3px solid {top_color};" if top_color else ""
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                padding:{padding};margin-bottom:{margin_bottom};{border_top}
                box-shadow:0 1px 4px rgba(28,43,74,.06)">
    """, unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def card_heading(text: str):
    st.markdown(f"""
    <p style="font-family:'Lora',serif;font-size:.93rem;font-weight:700;
              color:#1c2b4a;margin:0 0 1rem">{text}</p>
    """, unsafe_allow_html=True)

def card_section_label(text: str):
    st.markdown(f"""
    <p style="font-family:'Lora',serif;font-size:.85rem;font-weight:700;
              color:#1c2b4a;text-transform:uppercase;letter-spacing:.06em;
              margin:0 0 .9rem">{text}</p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MOCK DATA  — used until FastAPI backend is connected
# ─────────────────────────────────────────────────────────────────────────────
MOCK_EXTRACTED_INFO = {
    "name":  "Alex Johnson",
    "email": "alex.johnson@email.com",
    "phone": "+91 98765 43210",
    "skills": [
        "Python", "FastAPI", "LangChain", "PostgreSQL", "Docker",
        "React", "TensorFlow", "Git", "REST APIs", "Streamlit",
    ],
    "education": [
        {"degree": "B.Tech in Computer Science",
         "institute": "VTU, Bengaluru", "year": "2024"},
    ],
    "experience": [
        {"role": "Python Intern", "company": "TechCorp Solutions",
         "duration": "6 months",
         "description": "Built REST APIs using FastAPI and PostgreSQL. Implemented CI/CD pipelines."},
    ],
    "projects": [
        {"name": "Document Q&A Bot", "tech": "LangChain, ChromaDB, Ollama",
         "description": "RAG-based document Q&A system using local LLMs."},
        {"name": "Student Portal", "tech": "React, Node.js, MongoDB",
         "description": "Full-stack web app for college student management."},
    ],
}

MOCK_QUESTIONS = {
    "Technical": [
        "Explain synchronous vs asynchronous programming in Python. How have you applied this in your projects?",
        "Walk us through how a RAG pipeline works and how you implemented one using LangChain.",
        "How does ChromaDB store and retrieve vector embeddings? What are its advantages over FAISS?",
        "How would you design a REST endpoint in FastAPI that handles file uploads securely?",
        "When would you choose PostgreSQL over MongoDB? What are the key differences?",
    ],
    "Project-Based": [
        "Walk me through your 'Document Q&A Bot' project. What was the biggest technical challenge?",
        "How did you handle large documents that exceeded the LLM context window in your Q&A bot?",
        "What improvements would you make to your 'Student Portal' if you had more time?",
    ],
    "Behavioral": [
        "Tell me about a time you had to learn a new technology quickly to meet a deadline.",
        "Describe a situation where you disagreed with a team member's approach. How was it resolved?",
    ],
    "Situational": [
        "If you joined our team and discovered the codebase had no tests, what would you do?",
        "How would you explain vector embeddings to a non-technical stakeholder?",
    ],
}

CHIP_STYLES = [
    ("#fdf0ec", "#8f3515", "#e8bfb0"),
    ("#f0f4fd", "#1c4db5", "#bfcfee"),
    ("#fdf8ee", "#a07820", "#e8d9a0"),
    ("#f0fdf4", "#186a3b", "#a0dbb5"),
    ("#f5f3ff", "#5b21b6", "#c4b5fd"),
]

CATEGORY_STYLES = {
    "Technical":      {"top": "#b5451b", "bg": "#fdf0ec", "fg": "#8f3515", "bd": "#e8bfb0", "icon": "🔧"},
    "Project-Based":  {"top": "#1c4db5", "bg": "#f0f4fd", "fg": "#1c4db5", "bd": "#bfcfee", "icon": "🚀"},
    "Behavioral":     {"top": "#a07820", "bg": "#fdf8ee", "fg": "#a07820", "bd": "#e8d9a0", "icon": "🧠"},
    "Situational":    {"top": "#186a3b", "bg": "#f0fdf4", "fg": "#186a3b", "bd": "#a0dbb5", "icon": "🎯"},
}