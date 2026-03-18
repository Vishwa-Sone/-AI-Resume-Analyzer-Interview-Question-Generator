import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from shared import (inject_css, topbar, navbar, breadcrumb, section_title,
                    step_bar, divider_label, CATEGORY_STYLES)

st.set_page_config(
    page_title="Interview Questions — ResumeAI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()
topbar()
navbar("questions")

# ── GUARD ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("analysis_done"):
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem">
      <p style="font-size:2.5rem;margin-bottom:1rem">🔒</p>
      <h2 style="font-size:1.3rem;font-weight:700;margin-bottom:.6rem;
                 font-family:'Lora',serif">No Resume Analyzed Yet</h2>
      <p style="color:#6b6b7b;font-size:.9rem;margin-bottom:1.5rem">
        Please upload and analyze a resume first.
      </p>
    </div>
    """, unsafe_allow_html=True)
    _, c, _ = st.columns([2, 1.2, 2])
    with c:
        if st.button("Go to Upload →", key="guard_btn"):
            st.switch_page("pages/Upload_Resume.py")
    st.stop()

info = st.session_state.extracted_info
role = st.session_state.get("job_role", "the role")
qs   = st.session_state.get("interview_questions", {})

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
breadcrumb(["Home", "Upload", "Analysis", "Interview Questions"])
section_title("Interview Questions")
st.markdown(f"""
<p style="color:#6b6b7b;font-size:.92rem;margin:.4rem 0 1.8rem;line-height:1.7">
  Generated for
  <strong style="color:#1c2b4a">{info['name']}</strong>
  — applying as
  <em style="color:#b5451b">{role}</em>
</p>
""", unsafe_allow_html=True)
step_bar(4)

# ── STAT CARDS ────────────────────────────────────────────────────────────────
stat_cols = st.columns(4, gap="small")
for col, (cat, s) in zip(stat_cols, CATEGORY_STYLES.items()):
    count = len(qs.get(cat, []))
    with col:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2d9cc;border-radius:4px;
                    padding:1rem;text-align:center;border-top:3px solid {s['top']};
                    box-shadow:0 1px 3px rgba(28,43,74,.05)">
          <p style="font-family:'Lora',serif;font-size:1.6rem;font-weight:700;
                    color:{s['top']};margin:0">{count}</p>
          <p style="font-size:.73rem;color:#6b6b7b;margin:.15rem 0 0;
                    font-weight:700">{s['icon']} {cat}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

# ── QUESTIONS BY CATEGORY ─────────────────────────────────────────────────────
for cat, s in CATEGORY_STYLES.items():
    questions = qs.get(cat, [])
    if not questions:
        continue

    # Category label row
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:.7rem;margin:1.8rem 0 .7rem">
      <div style="background:{s['bg']};border:1px solid {s['bd']};color:{s['fg']};
                  font-weight:700;font-size:.77rem;letter-spacing:.05em;
                  text-transform:uppercase;padding:.22rem .8rem;border-radius:3px">
        {s['icon']} &nbsp;{cat}
      </div>
      <span style="font-size:.77rem;color:#a0a0b0;font-weight:600">
        {len(questions)} questions
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Accordion questions
    for i, q in enumerate(questions, 1):
        preview = q[:85] + ("..." if len(q) > 85 else "")
        with st.expander(f"Q{i}.  {preview}"):
            st.markdown(f"""
            <div style="padding:.4rem .2rem">
              <p style="font-size:.9rem;color:#1c2b4a;line-height:1.78;margin:0">
                {q}
              </p>
              <div style="border-top:1px solid #f0ece5;margin:.9rem 0 0;
                          padding-top:.7rem">
                <p style="font-size:.77rem;color:#a0a0b0;margin:0;font-style:italic">
                  Look for clarity of thought, practical examples,
                  and depth of understanding.
                </p>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── EXPORT SECTION ────────────────────────────────────────────────────────────
divider_label("Export & Actions")

total_q = sum(len(v) for v in qs.values())
st.markdown(f"""
<p style="font-size:.85rem;color:#6b6b7b;margin:0 0 1.2rem;line-height:1.6">
  Download all {total_q} questions as a plain text file to share with
  your hiring team or use during the interview.
</p>
""", unsafe_allow_html=True)

# ── BUILD DOWNLOAD TEXT ───────────────────────────────────────────────────────
txt  = f"INTERVIEW QUESTIONS — ResumeAI\n{'='*52}\n"
txt += f"Candidate : {info['name']}\n"
txt += f"Role      : {role}\n"
txt += f"{'='*52}\n"
for cat, s in CATEGORY_STYLES.items():
    questions = qs.get(cat, [])
    if not questions:
        continue
    txt += f"\n{cat.upper()}\n{'-'*30}\n"
    for i, q in enumerate(questions, 1):
        txt += f"{i}. {q}\n\n"

# ── ACTION BUTTONS — all outside HTML blocks ──────────────────────────────────
col_dl, col_new, col_back = st.columns([1, 1, 1])

with col_dl:
    st.download_button(
        label="⬇  Download as TXT",
        data=txt,
        file_name=f"interview_questions_{info['name'].replace(' ','_').lower()}.txt",
        mime="text/plain",
        key="download_btn",
    )

with col_new:
    if st.button("Analyze New Resume", key="restart_btn"):
        for k in ["analysis_done", "extracted_info", "uploaded_file_name",
                  "job_role", "job_description", "resume_bytes",
                  "interview_questions"]:
            st.session_state.pop(k, None)
        st.switch_page("pages/Upload_Resume.py")

with col_back:
    st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
    if st.button("← Back to Analysis", key="back_btn"):
        st.switch_page("pages/Analysis_Result.py")
    st.markdown('</div>', unsafe_allow_html=True)
