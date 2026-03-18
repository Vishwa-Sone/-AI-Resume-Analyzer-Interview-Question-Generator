import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from shared import (inject_css, topbar, navbar, breadcrumb, section_title,
                    step_bar, CHIP_STYLES)

st.set_page_config(
    page_title="Analysis Results — ResumeAI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()
topbar()
navbar("analysis")

# ── GUARD ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("analysis_done"):
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem">
      <p style="font-size:2.5rem;margin-bottom:1rem">🔒</p>
      <h2 style="font-size:1.3rem;font-weight:700;margin-bottom:.6rem;
                 font-family:'Lora',serif">No Analysis Found</h2>
      <p style="color:#6b6b7b;font-size:.9rem;margin-bottom:1.5rem">
        Please upload a resume first to see results.
      </p>
    </div>
    """, unsafe_allow_html=True)
    _, c, _ = st.columns([2, 1.2, 2])
    with c:
        if st.button("Go to Upload →", key="guard_btn"):
            st.switch_page("pages/Upload_Resume.py")
    st.stop()

info = st.session_state.extracted_info
role = st.session_state.get("job_role", "Not specified")

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
breadcrumb(["Home", "Upload", "Analysis Results"])
section_title("Analysis Results")
st.markdown("""
<p style="color:#6b6b7b;font-size:.92rem;margin:.4rem 0 1.8rem;line-height:1.7">
  AI-extracted information from the candidate's resume.
</p>
""", unsafe_allow_html=True)
step_bar(2)

# ── CANDIDATE HEADER CARD ─────────────────────────────────────────────────────
initial = info["name"][0].upper()
st.markdown(f"""
<div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
            border-top:3px solid #1c2b4a;padding:1.4rem 1.8rem;
            margin-bottom:1.2rem;display:flex;align-items:center;
            gap:1.4rem;flex-wrap:wrap;
            box-shadow:0 1px 4px rgba(28,43,74,.06)">
  <div style="background:#1c2b4a;border-radius:50%;width:52px;height:52px;
              display:flex;align-items:center;justify-content:center;
              font-family:'Lora',serif;font-weight:700;font-size:1.3rem;
              color:#c9973a;flex-shrink:0">{initial}</div>
  <div style="flex:1;min-width:180px">
    <h2 style="font-size:1.1rem;font-weight:700;margin:0 0 .25rem;
               font-family:'Lora',serif">{info['name']}</h2>
    <p style="margin:0;font-size:.83rem;color:#6b6b7b">
      📧 &nbsp;{info['email']} &nbsp;&nbsp;|&nbsp;&nbsp; 📞 &nbsp;{info['phone']}
    </p>
  </div>
  <div style="background:#faf8f5;border:1px solid #e2d9cc;border-radius:4px;
              padding:.55rem 1.1rem;text-align:center">
    <p style="margin:0;font-size:.67rem;color:#c9973a;font-weight:700;
              letter-spacing:.08em;text-transform:uppercase">Applying For</p>
    <p style="margin:.15rem 0 0;font-size:.9rem;font-weight:700;color:#1c2b4a">
      {role}
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SKILLS + RIGHT COLUMN ─────────────────────────────────────────────────────
col_skills, col_right = st.columns([1.1, 1], gap="medium")

with col_skills:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                border-top:3px solid #c9973a;padding:1.4rem;height:100%;
                box-shadow:0 1px 4px rgba(28,43,74,.06)">
      <p style="font-family:'Lora',serif;font-size:.85rem;font-weight:700;
                color:#1c2b4a;text-transform:uppercase;letter-spacing:.06em;
                margin:0 0 .9rem">Technical Skills</p>
    </div>
    """, unsafe_allow_html=True)

    chips = ""
    for i, skill in enumerate(info["skills"]):
        bg, fg, bd = CHIP_STYLES[i % len(CHIP_STYLES)]
        chips += (
            f'<span style="background:{bg};color:{fg};border:1px solid {bd};'
            f'border-radius:3px;padding:.22rem .7rem;font-size:.78rem;'
            f'font-weight:700;display:inline-block;margin:.22rem .18rem;'
            f'letter-spacing:.02em">{skill}</span>'
        )
    st.markdown(f"<div style='line-height:2.4'>{chips}</div>",
                unsafe_allow_html=True)

with col_right:
    # Education
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                border-top:3px solid #b5451b;padding:1.3rem;margin-bottom:1rem;
                box-shadow:0 1px 4px rgba(28,43,74,.06)">
      <p style="font-family:'Lora',serif;font-size:.85rem;font-weight:700;
                color:#1c2b4a;text-transform:uppercase;letter-spacing:.06em;
                margin:0 0 .8rem">Education</p>
    </div>
    """, unsafe_allow_html=True)

    for edu in info["education"]:
        st.markdown(f"""
        <div style="border-left:3px solid #b5451b;padding-left:.85rem;
                    margin-bottom:.6rem">
          <p style="margin:0;font-size:.87rem;font-weight:700;color:#1c2b4a">
            {edu['degree']}
          </p>
          <p style="margin:.1rem 0 0;font-size:.79rem;color:#6b6b7b">
            {edu['institute']} &nbsp;·&nbsp; {edu['year']}
          </p>
        </div>
        """, unsafe_allow_html=True)

    # Work Experience
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                border-top:3px solid #1c2b4a;padding:1.3rem;
                box-shadow:0 1px 4px rgba(28,43,74,.06)">
      <p style="font-family:'Lora',serif;font-size:.85rem;font-weight:700;
                color:#1c2b4a;text-transform:uppercase;letter-spacing:.06em;
                margin:0 0 .8rem">Work Experience</p>
    </div>
    """, unsafe_allow_html=True)

    for exp in info["experience"]:
        st.markdown(f"""
        <div style="border-left:3px solid #1c2b4a;padding-left:.85rem;
                    margin-bottom:.8rem">
          <p style="margin:0;font-size:.87rem;font-weight:700;color:#1c2b4a">
            {exp['role']}
          </p>
          <p style="margin:.1rem 0;font-size:.79rem;color:#c9973a;font-weight:700">
            {exp['company']} &nbsp;·&nbsp; {exp['duration']}
          </p>
          <p style="margin:0;font-size:.79rem;color:#6b6b7b;line-height:1.6">
            {exp['description']}
          </p>
        </div>
        """, unsafe_allow_html=True)

# ── PROJECTS ──────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
            border-top:3px solid #c9973a;padding:1.4rem;
            box-shadow:0 1px 4px rgba(28,43,74,.06)">
  <p style="font-family:'Lora',serif;font-size:.85rem;font-weight:700;
            color:#1c2b4a;text-transform:uppercase;letter-spacing:.06em;
            margin:0 0 1rem">Projects</p>
</div>
""", unsafe_allow_html=True)

proj_cols = st.columns(len(info["projects"]), gap="medium")
for col, proj in zip(proj_cols, info["projects"]):
    with col:
        st.markdown(f"""
        <div style="background:#faf8f5;border:1px solid #e2d9cc;
                    border-radius:4px;padding:1rem">
          <p style="font-family:'Lora',serif;margin:0 0 .25rem;font-size:.88rem;
                    font-weight:600;color:#1c2b4a">{proj['name']}</p>
          <p style="margin:0 0 .45rem;font-size:.76rem;color:#b5451b;
                    font-weight:700">{proj['tech']}</p>
          <p style="margin:0;font-size:.8rem;color:#6b6b7b;line-height:1.6">
            {proj['description']}
          </p>
        </div>
        """, unsafe_allow_html=True)

# ── ACTION BUTTONS ────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

# Inject alignment fix — forces both button wrappers to same height
st.markdown("""
<style>
.btn-row > div[data-testid="column"] {
    display: flex !important;
    align-items: center !important;
}
.btn-row > div[data-testid="column"] .stButton,
.btn-row > div[data-testid="column"] .stButton > button {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="btn-row">', unsafe_allow_html=True)
col_a, col_b, _ = st.columns([1, 1.5, 2])

with col_a:
    st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
    if st.button("← Re-upload Resume", key="reupload_btn"):
        st.session_state.analysis_done = False
        st.switch_page("pages/Upload_Resume.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    if st.button("Generate Interview Questions →", key="next_btn"):
        st.switch_page("pages/Interview_Questions.py")

st.markdown('</div>', unsafe_allow_html=True)
